#!/usr/bin/env python3
import argparse, os, re, subprocess, sys, math
from shutil import which

# --------------------------- utils ---------------------------

def need(cmd):
    if which(cmd) is None:
        sys.exit(f"❌ Required command not found: {cmd}")

def ffprobe_dims(path):
    need("ffprobe")
    try:
        out = subprocess.check_output([
            "ffprobe","-v","error","-select_streams","v:0",
            "-show_entries","stream=width,height",
            "-of","csv=s=x:p=0", path
        ], text=True).strip()
        w, h = out.split("x")
        return int(w), int(h)
    except Exception as e:
        sys.exit(f"❌ ffprobe failed on {path}: {e}")

def clamp(v, lo, hi): return max(lo, min(hi, v))

def parse_rgba(s, default_alpha=1.0):
    s = s.strip()
    if re.fullmatch(r"[A-Za-z]+(@[0-1]?(\.\d+)?)?", s):
        return s if "@" in s else f"{s}@{default_alpha}"
    if s.startswith("#"):
        hx=s[1:]
        if len(hx)==6:
            r=int(hx[0:2],16); g=int(hx[2:4],16); b=int(hx[4:6],16); a=default_alpha
        elif len(hx)==8:
            r=int(hx[0:2],16); g=int(hx[2:4],16); b=int(hx[4:6],16); a=int(hx[6:8],16)/255.0
        else:
            sys.exit("❌ Hex color must be #RRGGBB or #RRGGBBAA")
        return f"0x{r:02X}{g:02X}{b:02X}@{a:.6g}"
    if "," in s:
        parts=[p.strip() for p in s.split(",")]
        if len(parts) not in (3,4): sys.exit("❌ RGB(A) must be r,g,b[,a]")
        def to255(x):
            if "." in x: return max(0, min(255, int(round(float(x)*255))))
            return max(0, min(255, int(x)))
        r=to255(parts[0]); g=to255(parts[1]); b=to255(parts[2]); a=float(parts[3]) if len(parts)==4 else default_alpha
        return f"0x{r:02X}{g:02X}{b:02X}@{a:.6g}"
    sys.exit(f"❌ Unrecognized color format: {s}")

def build_position_expr(pos, pad):
    pad=int(pad)
    if pos=="tl": return f"{pad}", f"{pad}"
    if pos=="tr": return f"main_w-overlay_w-{pad}", f"{pad}"
    if pos=="bl": return f"{pad}", f"main_h-overlay_h-{pad}"
    if pos=="br": return f"main_w-overlay_w-{pad}", f"main_h-overlay_h-{pad}"
    if pos=="c":  return "(main_w-overlay_w)/2", "(main_h-overlay_h)/2"
    sys.exit("❌ Invalid --pos. Choose tl,tr,bl,br,c.")

def opposite_pos(pos):
    return {"tl":"br","tr":"bl","bl":"tr","br":"tl","c":"c"}[pos]

# ---------------------- shape + border -----------------------

def geq_rect_expr():     return "if(between(X,margin,W-1-margin)*between(Y,margin,H-1-margin),255,0)"
def geq_circle_expr():   return "if(lte(hypot(X-W/2,Y-H/2),min(W,H)/2-margin),255,0)"
def geq_rhombus_expr():  return "if(lte((abs(X-W/2)/max(W/2-margin,1)) + (abs(Y-H/2)/max(H/2-margin,1)),1),255,0)"
def geq_triangle_expr(): return "if((gte(Y/H,2*abs(X/W-0.5)+margin/H))*(lte(Y/H,1-margin/H)),255,0)"

def build_shape_mask_named(shape, W, H, margin_px, feather_px, name):
    """Return filtergraph segment that writes a gray mask labeled [name]."""
    margin_px=max(0, int(round(margin_px)))
    feather_px=max(0, int(round(feather_px)))
    if shape=="square":   expr=geq_rect_expr()
    elif shape=="circle": expr=geq_circle_expr()
    elif shape=="rhombus":expr=geq_rhombus_expr()
    elif shape=="triangle":expr=geq_triangle_expr()
    else: raise ValueError("Unsupported generated shape")

    seg  = f"color=c=black:s={W}x{H},format=gray[{name}_masksrc];"
    seg += f"[{name}_masksrc]geq=lum_expr='{expr}':cb_expr='128':cr_expr='128':alpha_expr='255',"
    seg  = seg.replace("margin", str(margin_px))
    if feather_px>0:
        sigma=max(0.1, feather_px/2.0)
        seg += f"gblur=sigma={sigma},"
    seg += f"format=gray[{name}];"
    return seg

def build_border_ring_named(shape, W, H, base_margin, border_px, name):
    if border_px<=0: return "", None
    base = shape if shape in {"square","circle","triangle","rhombus"} else "square"
    outer = build_shape_mask_named(base, W,H, base_margin, 0, name=f"{name}_outer")
    inner = build_shape_mask_named(base, W,H, base_margin+border_px, 0, name=f"{name}_inner")
    ring  = f"[{name}_outer][{name}_inner]blend=all_mode=difference,format=gray[{name}_ring];"
    return outer+inner+ring, f"[{name}_ring]"

# --------------------- animation helpers --------------------

def ease_expr(dur):
    # Smoothstep e = p*p*(3-2*p) with NO commas (so it’s safe even if you forget quotes)
    p = f"(t/{dur})"
    pe = f"if(lt({p},0),0, if(gt({p},1),1,{p}))"
    return f"({pe})*({pe})*(3-2*({pe}))"

def lerp_expr(start_expr, end_expr, dur):
    e = ease_expr(dur if dur>0 else 1e-6)
    return f"(({start_expr}) + (({end_expr})-({start_expr}))*{e})"

def start_end_exprs(pos, pad):
    sx, sy = build_position_expr(pos, pad)
    ex, ey = build_position_expr(opposite_pos(pos), pad)
    return (sx, sy, ex, ey)

# -------------------- per-PiP build chain -------------------

def build_single_pip_chain(idx, base_bg_label, src_label, tw, th, shape, feather_px,
                           border_px, border_color, rotate_deg,
                           lagfun_decay, fade_dur, pos, pad,
                           mask_label=None):
    name = f"p{idx}"
    parts=[]
    margin = max(0,int(round(feather_px)))

    # 1) scale → format
    parts.append(f"[{src_label}]scale={tw}:{th}:flags=lanczos,setsar=1[{name}_src];")
    cur = f"[{name}_src]"

    # 2) optional rotate
    if abs(rotate_deg)>1e-6:
        ang = rotate_deg*math.pi/180.0
        parts.append(f"{cur}rotate={ang:.10f}:ow=iw:oh=ih:fillcolor=black@0,format=yuv444p[{name}_rot];")
        cur=f"[{name}_rot]"

    # 3) optional lagfun (temporal smear)
    if lagfun_decay>0:
        d = max(0.0, min(1.0, float(lagfun_decay)))
        parts.append(f"{cur}format=yuv444p,lagfun=decay={d}[{name}_lag];")
        cur=f"[{name}_lag]"

    # 4) ensure exact size + RGBA
    parts.append(f"{cur}scale={tw}:{th}:flags=bicubic,setsar=1,format=rgba[{name}_rgba0];")
    cur=f"[{name}_rgba0]"

    # 5) build or use mask, then alphamerge
    if shape=="mask":
        parts.append(f"{mask_label}scale={tw}:{th},setsar=1,format=gray[{name}_mask];")
    else:
        parts.append(build_shape_mask_named(shape, tw, th, margin, feather_px, name=f"{name}_mask"))
    parts.append(f"{cur}[{name}_mask]alphamerge[{name}_rgba];")
    cur=f"[{name}_rgba]"

    # 6) fade-in alpha during travel
    if fade_dur>0:
        parts.append(f"{cur}fade=t=in:st=0:d={fade_dur}:alpha=1[{name}_fade];")
        cur=f"[{name}_fade]"

    pip_rgba = cur

    # 7) optional border underlay
    ring_chain, ring_label = build_border_ring_named(shape, tw, th, margin, border_px, name=f"{name}_b")
    if ring_chain: parts.append(ring_chain)
    if ring_label:
        col = parse_rgba(border_color,1.0)
        parts.append(f"color=c={col}:s={tw}x{th}:r=30,format=rgba[{name}_border_col];")
        parts.append(f"[{name}_border_col]{ring_label}alphamerge[{name}_border_rgba];")

    # 8) animated coordinates (x,y)
    sx, sy, ex, ey = start_end_exprs(pos, pad)
    xexpr = lerp_expr(sx, ex, fade_dur)
    yexpr = lerp_expr(sy, ey, fade_dur)

    # 9) compose: border first (if any), then PiP — QUOTE x/y
    acc_label = base_bg_label
    if ring_label:
        parts.append(f"{acc_label}[{name}_border_rgba]overlay=x='{xexpr}':y='{yexpr}':eval=frame[{name}_accb];")
        acc_label = f"[{name}_accb]"
    parts.append(f"{acc_label}{pip_rgba}overlay=x='{xexpr}':y='{yexpr}':format=auto:eval=frame[{name}_acc];")

    return "".join(parts), f"[{name}_acc]"

# ------------------- main command builder -------------------

def build_ffmpeg_cmd(bg, pip, out,
                     position="tr", pad=24,
                     pip_percent=30.0, pip_width=None, pip_height=None,
                     shape="square", mask_path=None, feather_px=16,
                     border_px=6, border_color="#FFFFFF",
                     pip_opacity=1.0,  # applied pre-compose
                     rotate_deg=0.0,
                     # Animation:
                     anim=True, anim_duration=1.5, lagfun_decay=0.0,
                     all_positions=False,
                     crf=18, preset="veryfast", audio="bg"):
    need("ffmpeg")
    if not os.path.isfile(bg):  sys.exit(f"❌ Background not found: {bg}")
    if not os.path.isfile(pip): sys.exit(f"❌ PiP not found: {pip}")
    if shape=="mask" and not mask_path: sys.exit("❌ shape=mask requires --mask")

    bg_w,bg_h = ffprobe_dims(bg)
    src_w,src_h = ffprobe_dims(pip)

    # target size
    if pip_width and pip_height:
        tw,th = int(pip_width), int(pip_height)
    elif pip_width:
        tw = int(pip_width); th = int(round(src_h*(tw/src_w)))
    elif pip_height:
        th = int(pip_height); tw = int(round(src_w*(th/src_h)))
    else:
        tw = int(round(bg_w * float(pip_percent)/100.0))
        th = int(round(src_h * (tw/src_w)))
    # clamp to even
    tw = (max(32, min(bg_w, tw)) // 2) * 2
    th = (max(32, min(bg_h, th)) // 2) * 2

    inputs = ["-y","-i",bg,"-i",pip]
    parts = []

    positions = ["tl","tr","bl","br","c"] if all_positions else [position]

    # mask for shape=mask (split per copy)
    if shape=="mask":
        inputs += ["-loop","1","-i",mask_path]
        parts.append(f"[2:v]split={len(positions)}" + "".join([f"[m{i}]" for i in range(len(positions))]) + ";")

    # base background
    parts.append("[0:v]format=yuv420p[bg0];")
    # split pip for each position
    parts.append(f"[1:v]split={len(positions)}" + "".join([f"[pip{i}]" for i in range(len(positions))]) + ";")

    last_acc = "[bg0]"
    for i, pos in enumerate(positions):
        mask_label = f"[m{i}]" if shape=="mask" else None
        chain, acc = build_single_pip_chain(
            idx=i,
            base_bg_label=last_acc,
            src_label=f"pip{i}",
            tw=tw, th=th,
            shape=shape, feather_px=feather_px,
            border_px=border_px, border_color=border_color,
            rotate_deg=rotate_deg,
            lagfun_decay=(lagfun_decay if anim else 0.0),
            fade_dur=(anim_duration if anim else 0.0),
            pos=pos, pad=pad,
            mask_label=mask_label
        )
        # apply optional overall opacity BEFORE compositing next ones
        if pip_opacity < 1.0:
            a = clamp(pip_opacity,0.0,1.0)
            chain += f"[p{i}_fade]format=rgba,colorchannelmixer=aa={a:.6g}[p{i}_fade];".replace(f"p{i}_fade", f"p{i}_fade")
        parts.append(chain)
        last_acc = acc

    # final video stream
    parts.append(f"{last_acc}format=yuv420p[outv];")

    # audio
    map_audio=[]
    if audio=="bg":   map_audio=["-map","0:a?"]
    elif audio=="pip":map_audio=["-map","1:a?"]
    elif audio=="mix":
        parts.append(";[0:a][1:a]amix=inputs=2:dropout_transition=0:normalize=0[outa]")
        map_audio=["-map","[outa]"]
    elif audio=="none": map_audio=[]

    graph="".join(parts)

    cmd=["ffmpeg"]+inputs+[
        "-filter_complex", graph,
        "-map","[outv]"
    ]+map_audio+[
        "-c:v","libx264",
        "-pix_fmt","yuv420p",
        "-profile:v","high","-level:v","4.1",
        "-movflags","+faststart",
        "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",
        "-crf",str(crf), "-preset",preset,
        "-shortest",
        out
    ]
    return cmd

# ------------------------------ CLI ------------------------------

def main():
    p=argparse.ArgumentParser(description="FFmpeg PiP with animated travel+fade, optional lagfun, shapes/border, and multi-position mode.")
    p.add_argument("-i","--input",required=True, help="Background video")
    p.add_argument("-p","--pip",required=True, help="PiP (overlay) video")
    p.add_argument("-o","--output",required=True)

    p.add_argument("--pos",default="tr",choices=["tl","tr","bl","br","c"], help="Start position if not using --all-positions")
    p.add_argument("--pad",type=int,default=24, help="Padding (pixels)")

    g=p.add_argument_group("Size")
    g.add_argument("--pip-percent",type=float,default=30.0, help="PiP width as % of BG width")
    g.add_argument("--pip-width",type=int)
    g.add_argument("--pip-height",type=int)

    s=p.add_argument_group("Shape/Mask")
    s.add_argument("--shape",default="square",choices=["square","circle","triangle","rhombus","mask"])
    s.add_argument("--mask",help="External mask (white=opaque, black=transparent) when shape=mask")
    s.add_argument("--feather",type=int,default=16,help="Feather width (px)")

    b=p.add_argument_group("Border")
    b.add_argument("--border-width",type=int,default=6)
    b.add_argument("--border-color",default="#FFFFFF")

    t=p.add_argument_group("Transform")
    t.add_argument("--rotate",type=float,default=0.0,help="Rotate PiP content (deg clockwise)")

    a=p.add_argument_group("Animation")
    a.add_argument("--no-anim",dest="anim",action="store_false", help="Disable travel+fade animation")
    a.add_argument("--anim-duration",type=float,default=1.5, help="Seconds for travel+fade")
    a.add_argument("--lagfun-decay",type=float,default=0.0, help="0..1 temporal lagfun amount (0=off)")
    a.add_argument("--all-positions",action="store_true", help="Animate 5 PiPs from each start to its opposite")

    e=p.add_argument_group("Encode/Audio")
    e.add_argument("--crf",type=int,default=18)
    e.add_argument("--preset",default="veryfast")
    p.add_argument("--pip-opacity",type=float,default=1.0,help="Final static opacity 0..1")
    p.add_argument("--audio",default="bg",choices=["bg","pip","mix","none"])

    a=p.parse_args()
    cmd=build_ffmpeg_cmd(
        bg=a.input, pip=a.pip, out=a.output,
        position=a.pos, pad=a.pad,
        pip_percent=a.pip_percent, pip_width=a.pip_width, pip_height=a.pip_height,
        shape=a.shape, mask_path=a.mask, feather_px=a.feather,
        border_px=a.border_width, border_color=a.border_color,
        pip_opacity=a.pip_opacity,
        rotate_deg=a.rotate,
        anim=a.anim, anim_duration=a.anim_duration, lagfun_decay=a.lagfun_dec
ay,
        all_positions=a.all_positions,
        crf=a.crf, preset=a.preset, audio=a.audio
    )
    print("▶️ FFmpeg:\n", " ".join([subprocess.list2cmdline([c]) if " " in c else c for c in cmd]), "\n")
    r=subprocess.run(cmd)
    if r.returncode!=0: sys.exit(f"❌ FFmpeg failed with code {r.returncode}")
    print(f"✅ Done: {a.output}")

if __name__=="__main__":
    main()
