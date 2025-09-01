#!/usr/bin/env python3
import argparse, subprocess, random, shlex, sys, os, re, math

# ----------------------------
# Motion expressions (FFmpeg)
# ----------------------------
def motion_expr(pattern, sx, sy, W="W", H="H", w="w", h="h"):
    if pattern == "pingpong":
        ex = f"({W}-{w})*abs(mod((t/{max(sx,1e-6)})*2,2)-1)"
        ey = f"({H}-{h})*abs(mod((t/{max(sy,1e-6)})*2,2)-1)"
    elif pattern == "sine":
        ex = f"({W}-{w})*(0.5+0.5*sin(2*PI*t/{max(sx,1e-6)}))"
        ey = f"({H}-{h})*(0.5+0.5*cos(2*PI*t/{max(sy,1e-6)}))"
    elif pattern == "wrap":
        ex = f"mod(t*{sx}, {W}-{w})"
        ey = f"mod(t*{sy}, {H}-{h})"
    elif pattern == "lissajous":
        ex = f"({W}-{w})*(0.5+0.5*sin(2*PI*t/{max(sx,1e-6)}))"
        ey = f"({H}-{h})*(0.5+0.5*sin(2*PI*t/{max(sy,1e-6)} + PI/2))"
    elif pattern == "gravity":
        ex = f"({W}-{w})*(0.5+0.5*sin(2*PI*{sx}*t))"
        ey = f"({H}-{h})*(abs(sin(2*PI*{sx}*t))*exp(-{max(sy,0)}*t))"
    # Extra patterns
    elif pattern == "circle":
        ex = f"({W}-{w})*(0.5+0.5*cos(2*PI*t/{max(sx,1e-6)}))"
        ey = f"({H}-{h})*(0.5+0.5*sin(2*PI*t/{max(sy,1e-6)}))"
    elif pattern == "ellipse":
        ex = f"({W}-{w})*(0.5+0.5*cos(2*PI*t/{max(sx,1e-6)}))"
        ey = f"({H}-{h})*(0.5+0.5*0.7*sin(2*PI*t/{max(sy,1e-6)}))"
    elif pattern == "figure8":
        ex = f"({W}-{w})*(0.5+0.5*sin(2*PI*t/{max(sx,1e-6)}))"
        ey = f"({H}-{h})*(0.5+0.5*sin(4*PI*t/{max(sy,1e-6)}))"
    elif pattern == "rose3":
        ang = f"(2*PI*t/{max(sx,1e-6)})"
        r   = f"(0.4*(1+sin(3*{ang})))"
        ex = f"({W}-{w})*(0.5+{r}*cos({ang}))"
        ey = f"({H}-{h})*(0.5+{r}*sin({ang}))"
    else:
        raise ValueError("Unknown pattern")
    return ex, ey

def _hex_to_rgb0x(s):
    s = s.strip()
    if s.startswith("#"): s = s[1:]
    if not re.fullmatch(r"[0-9a-fA-F]{6}", s):
        raise ValueError(f"Bad hex color: {s}")
    return "0x" + s.upper()

def _eq_chain(bright, contrast, saturation, gamma):
    # Defaults: 0/1/1/1 ⇒ no-op
    parts = []
    if bright != 0.0:      parts.append(f"brightness={bright}")
    if contrast != 1.0:    parts.append(f"contrast={contrast}")
    if saturation != 1.0:  parts.append(f"saturation={saturation}")
    if gamma != 1.0:       parts.append(f"gamma={gamma}")
    return ("," + "eq=" + ":".join(parts)) if parts else ""

def build_filtergraph(args, T=None):
    W, H = args.res.split("x")
    fps = args.fps
    tcap = f"if(lt(t,{T}),t,{T})" if (args.duration_mode == "freeze" and T is not None) else "t"

    motion_on = (args.motion == "on")

    # Motion expressions if needed
    if motion_on:
        ex, ey = motion_expr(args.pattern, args.speed_x, args.speed_y, "W","H","w","h")
        if tcap != "t":
            ex = ex.replace("t", tcap)
            ey = ey.replace("t", tcap)
        if args.randomize:
            patterns = ["pingpong","sine","wrap","lissajous","gravity","circle","ellipse","figure8","rose3"]
            chosen = random.choice(patterns)
            ex, ey = motion_expr(chosen, args.speed_x, args.speed_y, "W","H","w","h")
            if tcap != "t":
                ex = ex.replace("t", tcap)
                ey = ey.replace("t", tcap)
    else:
        ex = "(W-w)/2"; ey = "(H-h)/2"

    # Trails only when moving
    trail_chain = []
    if motion_on:
        if args.decay is not None:
            trail_chain.append(f"lagfun=decay={args.decay}")
        if args.delay_frames and args.delay_frames > 0:
            trail_chain.append(f"tmix=frames={args.delay_frames}")
        if args.trail_blur and args.trail_blur > 0:
            trail_chain.append(f"gblur=sigma={args.trail_blur}")
    trail_chain_str = ",".join(trail_chain) if trail_chain else "null"

    # Spin only when moving
    spin_ang_expr = None
    if motion_on and args.spin_period > 0:
        phase = args.spin_phase_deg * math.pi / 180.0
        spin_ang_expr = f"(2*PI*({tcap})/{args.spin_period} + {phase})"

    # Foreground EQ chain
    eqc = _eq_chain(args.fg_brightness, args.fg_contrast, args.fg_saturation, args.fg_gamma)

    g = []
    # Background to canvas
    g.append(f"[1:v]scale={W}:{H},fps={fps}[bg]")

    if args.mode == "mask":
        # FG to canvas + optional EQ
        g.append(f"[0:v]scale={W}:{H},format=rgba,fps={fps}{eqc}[fgraw]")

        if motion_on:
            # moving small mask (original behavior)
            if args.mask:
                g.append(f"[2:v]fps={fps},scale={args.mask_size}:-1:flags=lanczos,format=gray,boxblur=2:1[m_gray]")
                if args.mask_key_type != "none":
                    kcol = _hex_to_rgb0x(args.mask_key_color)
                    g.append(f"[2:v]fps={fps},scale={args.mask_size}:-1:flags=lanczos,format=rgba[m_rgba]")
                    if args.mask_key_type == "colorkey":
                        g.append(f"[m_rgba]colorkey={kcol}:{args.mask_key_similarity}:{args.mask_key_blend},format=rgba[m_keyed]")
                    else:
                        g.append(f"[m_rgba]chromakey={kcol}:{args.mask_key_similarity}:{args.mask_key_blend},format=rgba[m_keyed]")
                    g.append(f"[m_keyed]alphaextract[m_key_a]")
                    g.append(f"[m_gray][m_key_a]blend=all_mode=normal:all_opacity={args.mask_key_mix}[m0]")
                else:
                    g.append(f"[m_gray]copy[m0]")
            else:
                g.append(f"color=c=white:s={args.mask_size}x{args.mask_size}:r={fps},format=gray[m0]")

            if spin_ang_expr:
                g.append(f"[m0]rotate=angle='{spin_ang_expr}':fillcolor=black@0:ow='rotw(iw)':oh='roth(ih)'[m0r]")
            else:
                g.append(f"[m0]copy[m0r]")

            g.append(f"color=c=black:s={W}x{H}:r={fps},format=gray[a0]")
            g.append(f"[a0][m0r]overlay=x='{ex}':y='{ey}':eval=frame,format=gray[a1]")

            g.append(f"[a1]{trail_chain_str},format=gray[atrail]")
            g.append(f"[fgraw][atrail]alphamerge[fgm]")

        else:
            # NON-MOTION: full-frame matte path (your example)
            if args.mask:
                blur = f",boxblur={args.mask_blur}:1" if args.mask_blur > 0 else ""
                g.append(f"[2:v]fps={fps},scale={W}:{H},format=gray{blur}[a1]")
            else:
                g.append(f"color=c=white:s={W}x{H}:r={fps},format=gray[a1]")
            g.append(f"[fgraw][a1]alphamerge[fgm]")

        # Optional alpha multiplier (aa)
        if args.alpha_mul != 1.0:
            g.append(f"[fgm]format=rgba,colorchannelmixer=aa={args.alpha_mul}[fg]")
        else:
            g.append(f"[fgm]copy[fg]")

        if args.alpha_out:
            g.append(f"color=c=black@0.0:s={W}x{H}:r={fps},format=rgba[zc]")
            g.append(f"[zc][fg]overlay=0:0:eval=frame[out]")
        else:
            g.append(f"[bg][fg]overlay=0:0:eval=frame[out]")

    elif args.mode == "sprite":
        # Sprite path (apply EQ to sprite too)
        g.append(f"[0:v]fps={fps},scale={args.mask_size}:-1:flags=lanczos,format=rgba[s0]")
        if eqc:
            g.append(f"[s0]{eqc[1:]}[s0eq]")   # eqc starts with ",", remove it
            src = "s0eq"
        else:
            src = "s0"

        if spin_ang_expr:
            g.append(f"[{src}]rotate=angle='{spin_ang_expr}':fillcolor=black@0:ow='rotw(iw)':oh='roth(ih)'[s0r]")
            g.append(f"[s0r]format=gray[sm]")
        else:
            g.append(f"[{src}]copy[s0r]")
            g.append(f"[{src}]format=gray[sm]")

        g.append(f"color=c=black@0.0:s={W}x{H}:r={fps},format=rgba[zc]")
        g.append(f"[zc][s0r]overlay=x='{ex}':y='{ey}':eval=frame[splaced]")

        g.append(f"color=c=black:s={W}x{H}:r={fps},format=gray[a0]")
        g.append(f"[a0][sm]overlay=x='{ex}':y='{ey}':eval=frame,format=gray[a1]")

        if motion_on and trail_chain_str != "null":
            g.append(f"[a1]{trail_chain_str},format=gray[atrail]")
        else:
            g.append(f"[a1]copy[atrail]")

        g.append(f"[splaced][atrail]alphamerge[spr]")

        if args.alpha_mul != 1.0:
            g.append(f"[spr]format=rgba,colorchannelmixer=aa={args.alpha_mul}[fg]")
        else:
            g.append(f"[spr]copy[fg]")

        if args.alpha_out:
            g.append(f"[fg]format=rgba[out]")
        else:
            g.append(f"[bg][fg]overlay=0:0:eval=frame[out]")
    else:
        raise ValueError("mode must be 'mask' or 'sprite'")

    return ";".join(g)

def probe_duration(infile):
    try:
        out = subprocess.check_output(
            ["ffprobe","-v","error","-select_streams","v:0",
             "-show_entries","stream=duration","-of","default=nw=1:nk=1", infile],
            text=True).strip()
        return float(out) if out else None
    except Exception:
        return None

def probe_has_audio(path: str) -> bool:
    try:
        out = subprocess.check_output(
            ["ffprobe","-v","error","-select_streams","a",
             "-show_entries","stream=index","-of","csv=p=0", path],
            text=True).strip()
        return bool(out)
    except Exception:
        return False

def main():
    p = argparse.ArgumentParser(description="Bounce/sprite compositor with motion on/off, full-frame mask matte, EQ, spin, trails, keying, and flexible audio.")
    p.add_argument("-i","--input", required=True, help="Foreground video (FG).")
    p.add_argument("-o","--output", required=True, help="Output file.")
    p.add_argument("-b","--background", default="bg.mp4", help="Background video/image.")
    p.add_argument("-m","--mask", help="Mask image/video (mask mode).")
    p.add_argument("--mode", choices=["mask","sprite"], default="mask")
    p.add_argument("--motion", choices=["on","off"], default="on", help="XY motion/spin/trails on (default) or static matte/sprite.")
    p.add_argument("--res", default="1280x720")
    p.add_argument("--fps", type=int, default=30)

    # Motion
    p.add_argument("--pattern", choices=["pingpong","sine","wrap","lissajous","gravity","circle","ellipse","figure8","rose3"], default="sine")
    p.add_argument("--randomize", action="store_true")
    p.add_argument("--speed-x", type=float, default=4.0)
    p.add_argument("--speed-y", type=float, default=6.0)

    # Size & trails
    p.add_argument("--mask-size", type=int, default=420)
    p.add_argument("--decay", type=float, default=0.88)
    p.add_argument("--delay-frames", type=int, default=0)
    p.add_argument("--trail-blur", type=float, default=0.0)

    # Spin
    p.add_argument("--spin-period", type=float, default=0.0)
    p.add_argument("--spin-phase-deg", type=float, default=0.0)

    # Output / formats
    p.add_argument("--alpha-out", action="store_true")
    p.add_argument("--codec", default="")
    p.add_argument("--pixfmt", default="")
    p.add_argument("--crf", type=int, default=18)
    p.add_argument("--preset", default="veryfast")
    p.add_argument("--duration-mode", choices=["shortest","freeze"], default="shortest")

    # Mask keying
    p.add_argument("--mask-key-type", choices=["none","colorkey","chromakey"], default="none")
    p.add_argument("--mask-key-color", default="#00FF00")
    p.add_argument("--mask-key-similarity", type=float, default=0.25)
    p.add_argument("--mask-key-blend", type=float, default=0.08)
    p.add_argument("--mask-key-mix", type=float, default=1.0)

    # NEW: Full-frame mask controls (non-motion)
    p.add_argument("--mask-fullframe", action="store_true", help="Use the mask as a full-frame matte (best with --motion off).")
    p.add_argument("--mask-blur", type=float, default=0.0, help="Boxblur radius for full-frame mask (pixels).")

    # NEW: Foreground EQ (applies pre-alpha)
    p.add_argument("--fg-brightness", type=float, default=0.0)
    p.add_argument("--fg-contrast", type=float, default=1.0)
    p.add_argument("--fg-saturation", type=float, default=1.0)
    p.add_argument("--fg-gamma", type=float, default=1.0)

    # NEW: Alpha multiplier
    p.add_argument("--alpha-mul", type=float, default=1.0, help="Multiply final alpha (e.g., 0.85).")

    # Audio
    p.add_argument("--audio-mode", choices=["auto","mix","1","2","none"], default="auto")

    args = p.parse_args()

    inputs = ["-i", args.input, "-i", args.background]
    if args.mode == "mask" and args.mask:
        inputs += ["-i", args.mask]

    T = probe_duration(args.input) if args.duration_mode == "freeze" else None
    has_a0 = probe_has_audio(args.input)
    has_a1 = probe_has_audio(args.background)

    fgraph = build_filtergraph(args, T)

    vcodec = args.codec or ("libvpx-vp9" if args.alpha_out else "libx264")
    pixfmt = args.pixfmt or ("yuva420p" if args.alpha_out else "yuv420p")
    extra = ["-auto-alt-ref","0"] if (args.alpha_out and vcodec == "libvpx-vp9") else []

    # ----- AUDIO MODES -----
    filter_complex_arg = fgraph
    map_args = []

    if args.alpha_out or args.audio_mode == "none":
        map_args = ["-map","[out]"]
    else:
        mode = args.audio_mode
        if mode == "auto":
            if has_a0 and has_a1:
                filter_complex_arg += ";[0:a][1:a]amix=inputs=2:dropout_transition=200:normalize=0,aformat=sample_fmts=fltp:channel_layouts=stereo,aresample=async=1[aout]"
                map_args = ["-map","[out]","-map","[aout]","-c:a","aac"]
            elif has_a0:
                map_args = ["-map","[out]","-map","0:a:0","-c:a","aac"]
            elif has_a1:
                map_args = ["-map","[out]","-map","1:a:0","-c:a","aac"]
            else:
                filter_complex_arg += ";anullsrc=r=48000:cl=stereo[aout]"
                map_args = ["-map","[out]","-map","[aout]","-c:a","aac"]

        elif mode == "mix":
            if has_a0 and has_a1:
                filter_complex_arg += ";[0:a][1:a]amix=inputs=2:dropout_transition=200:normalize=0,aformat=sample_fmts=fltp:channel_layouts=stereo,aresample=async=1[aout]"
                map_args = ["-map","[out]","-map","[aout]","-c:a","aac"]
            elif has_a0:
                map_args = ["-map","[out]","-map","0:a:0","-c:a","aac"]
            elif has_a1:
                map_args = ["-map","[out]","-map","1:a:0","-c:a","aac"]
            else:
                filter_complex_arg += ";anullsrc=r=48000:cl=stereo[aout]"
                map_args = ["-map","[out]","-map","[aout]","-c:a","aac"]

        elif mode == "1":
            if has_a0:
                map_args = ["-map","[out]","-map","0:a:0","-c:a","aac"]
            else:
                filter_complex_arg += ";anullsrc=r=48000:cl=stereo[aout]"
                map_args = ["-map","[out]","-map","[aout]","-c:a","aac"]

        elif mode == "2":
            if has_a1:
                map_args = ["-map","[out]","-map","1:a:0","-c:a","aac"]
            else:
                filter_complex_arg += ";anullsrc=r=48000:cl=stereo[aout]"
                map_args = ["-map","[out]","-map","[aout]","-c:a","aac"]

    cmd = ["ffmpeg","-y"] + inputs + ["-filter_complex", filter_complex_arg] + map_args + [
        "-c:v", vcodec, "-pix_fmt", pixfmt, "-crf", str(args.crf), "-preset", args.preset
    ]
    if args.duration_mode == "shortest":
        cmd += ["-shortest"]
    cmd += extra + [args.output]

    print("\n>>> Running:\n" + " ".join(shlex.quote(c) for c in cmd) + "\n")
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
