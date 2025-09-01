# videobeaux/programs/dynakey.py
# Keyer that respects Videobeaux GLOBALS (-i/-o/-F/-h come from the CLI).
# MP4-only output (libx264, yuv420p), optional background video or solid fill.
# Dynamic mode smoothly morphs similarity/blend over time.

from videobeaux.utils.ffmpeg_operations import run_ffmpeg_with_progress

def register_arguments(parser):
    parser.description = (
        "Dynamic Color/Chroma Keyer (FFmpeg) with despill, alpha-edge soften, solid/bg compositing, and art modes."
    )
    print("✅ dynakey ready. Use global -i/-o/-F. This mode adds only feature flags.")

    # Key engine + params
    parser.add_argument("--engine", choices=["colorkey", "chromakey"], default="colorkey",
                        help="colorkey=RGB distance; chromakey=YUV chroma distance (more broadcast-like).")
    parser.add_argument("--key", default="0x00FF00",
                        help="Key color. colorkey: 0xRRGGBB (e.g., 0x00FF00). chromakey: g/b/r or hex.")
    parser.add_argument("--similarity", type=float, default=0.12,
                        help="Color distance threshold to remove (~0.05–0.4 typical).")
    parser.add_argument("--blend", type=float, default=0.02,
                        help="Edge feather (0–1).")

    # Soften keyed edges by blurring alpha only
    parser.add_argument("--soften", type=float, default=0.0,
                        help="Extra edge soften in pixels (alpha-only blur).")

    # Spill + pre
    parser.add_argument("--despill", action="store_true", help="Reduce green/blue spill halos on edges.")
    parser.add_argument("--pre-denoise", action="store_true", help="Mild denoise before key (hqdn3d).")
    parser.add_argument("--pre-smooth-chroma", action="store_true",
                        help="Light chroma smoothing before key (yuv444p + blur).")

    # Background composition (video or solid color)
    parser.add_argument("--bg", help="Optional background VIDEO path (composite keyed FG over it).")
    parser.add_argument("--bg-solid", default="black",
                        help="Solid background if no --bg. Accepts names (black, white) or hex (#RRGGBB/0xRRGGBB).")

    # Art modes (post-key stylization)
    parser.add_argument("--art", choices=["none", "trails", "lighten-feedback"], default="none",
                        help="Stylize after key: 'trails' (lagfun) or 'lighten-feedback' (tblend).")
    parser.add_argument("--art-intensity", type=float, default=0.96,
                        help="Trails decay (0.85–0.995).")

    # Dynamic morphing (no-ZMQ): sweep similarity/blend over N segments
    parser.add_argument("--dynamic", action="store_true", help="Morph key params over time, then xfade between variants.")
    parser.add_argument("--segments", type=int, default=4, help="Number of morph segments (>=2).")
    parser.add_argument("--cycle-sim-min", type=float, default=0.08, help="Min similarity in morph.")
    parser.add_argument("--cycle-sim-max", type=float, default=0.25, help="Max similarity in morph.")
    parser.add_argument("--cycle-blend-min", type=float, default=0.0, help="Min blend in morph.")
    parser.add_argument("--cycle-blend-max", type=float, default=0.08, help="Max blend in morph.")

    # Output cadence
    parser.add_argument("--fps", type=float, default=30, help="Output FPS (default 30).")


def _norm_hex(s: str) -> str:
    """Normalize color strings to FFmpeg-friendly forms."""
    s = s.strip()
    if s.startswith("#"):
        return "0x" + s[1:]
    return s


def _key_filter(engine, key, similarity, blend):
    """Return filter that keys to RGBA (alpha created)."""
    if engine == "chromakey":
        return f"chromakey={key}:{similarity}:{blend},format=rgba"
    return f"colorkey={key}:{similarity}:{blend},format=rgba"


def _post_art(mode, intensity):
    if mode == "trails":
        return f",lagfun=decay={float(intensity)}"
    if mode == "lighten-feedback":
        return ",tblend=all_mode=lighten"
    return ""


def run(args):
    # ---------- Build pre-chain ----------
    pre = []
    if args.pre_denoise:
        pre.append("hqdn3d=l=2.0:c=1.5")
    if args.pre_smooth_chroma:
        pre.append("format=yuv444p,boxblur=0:1")
    pre_chain = (",".join(pre) + ",") if pre else ""

    # ---------- Foreground key(s) ----------
    graph = []
    key_color = _norm_hex(args.key)

    def keyed_stream(src_label, sim, blnd, out_label):
        chain = _key_filter(args.engine, key_color, sim, blnd)
        # alpha-only soften using gblur planes=a (avoids label collisions)
        if args.soften and args.soften > 0:
            chain += f",gblur=sigma={float(args.soften)}:steps=1:planes=a"
        if args.despill:
            chain += ",despill"
        chain += _post_art(args.art, args.art_intensity)
        graph.append(f"[{src_label}]{chain}[{out_label}]")

    if not args.dynamic:
        graph.append(f"[0:v]{pre_chain}setpts=PTS-STARTPTS[pre]")
        keyed_stream("pre", args.similarity, args.blend, "FG")
        fg_out = "FG"
    else:
        N = max(2, int(args.segments))
        graph.append(f"[0:v]{pre_chain}setpts=PTS-STARTPTS,format=yuv420p[pre]")
        graph.append(f"[pre]split={N}" + "".join(f"[s{i}]" for i in range(N)))

        def lerp(a, b, i, n): return a if n <= 1 else (a + (b - a) * (i / (n - 1)))
        segs = []
        for i in range(N):
            sim_i = round(lerp(args.cycle_sim_min, args.cycle_sim_max, i, N), 4)
            bln_i = round(lerp(args.cycle_blend_min, args.cycle_blend_max, i, N), 4)
            outl = f"K{i}"
            keyed_stream(f"s{i}", sim_i, bln_i, outl)
            segs.append(outl)

        # xfade through segments for a smooth morph (1s fades starting at 1s)
        cur = segs[0]
        for idx, nxt in enumerate(segs[1:], start=1):
            outl = f"XF{idx}"
            graph.append(f"[{cur}][{nxt}]xfade=transition=fade:duration=1.0:offset=1.0[{outl}]")
            cur = outl
        fg_out = cur

    # ---------- Background (video or solid) & composite ----------
    if args.bg:
        # Use provided background video; scale to FG dimensions using scale2ref, then overlay FG (RGBA) over BG.
        graph.append(f"[1:v]setpts=PTS-STARTPTS[BG0]")
        graph.append(f"[BG0][{fg_out}]scale2ref[BG][FGref]")  # BG resized to FG size
        graph.append(f"[BG][{fg_out}]overlay=shortest=1:format=auto[out_v]")
        need_bg_input = True
    else:
        # Create solid background sized to FG with scale2ref, then overlay.
        solid = _norm_hex(args.bg_solid)
        graph.append(f"color=c={solid}:s=16x16:d=1[BGsrc]")
        graph.append(f"[BGsrc][{fg_out}]scale2ref[BG][FGref]")
        graph.append(f"[BG][{fg_out}]overlay=shortest=1:format=auto[out_v]")
        need_bg_input = False

    filter_complex = ";".join(graph)

    # ---------- FFmpeg command (MP4 only; globals provide -i/-o/-F) ----------
    command = ["ffmpeg", "-i", args.input]
    if need_bg_input:
        command += ["-i", args.bg]
    command += [
        "-filter_complex", filter_complex,
        "-map", "[out_v]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-profile:v", "high",
        "-level:v", "4.2",
        "-pix_fmt", "yuv420p",
        "-r", str(args.fps),
        "-movflags", "+faststart",
        "-shortest",
        args.output,  # NOTE: your CLI states 'no extension'; we honor whatever it passes here.
    ]

    run_ffmpeg_with_progress(
        (command[:1] + ["-y"] + command[1:]) if getattr(args, "force", False) else command,
        args.input,
        args.output
    )
