#!/usr/bin/env python3
import argparse, os, re, subprocess, sys, math
from shutil import which

# --------------------- utils ---------------------

CSS_COLOR_NAMES = {
    "black":"#000000","white":"#FFFFFF","red":"#FF0000","green":"#00FF00","blue":"#0000FF",
    "yellow":"#FFFF00","magenta":"#FF00FF","cyan":"#00FFFF","gray":"#808080","grey":"#808080",
    "orange":"#FFA500","purple":"#800080","pink":"#FFC0CB","teal":"#008080","lime":"#00FF00",
}

def need(cmd):
    if which(cmd) is None:
        sys.exit(f"❌ Required command not found: {cmd}")

def ffprobe_dims(path):
    need("ffprobe")
    try:
        out = subprocess.check_output([
            "ffprobe","-v","error","-select_streams","v:0",
            "-show_entries","stream=width,height","-of","csv=s=x:p=0", path
        ], text=True).strip()
        w,h = out.split("x")
        return int(w), int(h)
    except Exception as e:
        sys.exit(f"❌ Could not read video dimensions for {path}: {e}")

def parse_hex_rgba(color_str, default_alpha=255):
    """
    Accepts #RRGGBB, #RRGGBBAA, or CSS color name (e.g., 'red').
    Returns (r,g,b,a) in 0..255
    """
    if not color_str:
        return (255,255,255, default_alpha)
    s = color_str.strip()
    if not s.startswith("#") and re.fullmatch(r"[A-Za-z]+", s):
        s = CSS_COLOR_NAMES.get(s.lower(), "#FFFFFF")
    if s.startswith("#"): s = s[1:]
    if not re.fullmatch(r"[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?", s):
        return (255,255,255, default_alpha)
    if len(s)==6:
        r=int(s[0:2],16); g=int(s[2:4],16); b=int(s[4:6],16); a=default_alpha
    else:
        r=int(s[0:2],16); g=int(s[2:4],16); b=int(s[4:6],16); a=int(s[6:8],16)
    return (r,g,b,a)

# --------------------- shape geq expressions ---------------------

def geq_rect_expr():
    return "255*gte(X,margin)*gte(Y,margin)*gte(W-1-margin,X)*gte(H-1-margin,Y)"

def geq_circle_expr():
    return "255*lte((X-W/2)*(X-W/2)+(Y-H/2)*(Y-H/2),((min(W,H)/2)-margin)*((min(W,H)/2)-margin))"

def geq_rhombus_expr():
    return "255*lte(abs(X-W/2)+abs(Y-H/2),(min(W,H)/2)-margin)"

def geq_triangle_expr():
    return "255*gte(Y,margin)*lte(Y,H-1-margin)*gte(X,(W/2)-(Y*(W/(2*H))))*lte(X,(W/2)+(Y*(W/(2*H))))"

# --------------------- mask builders ---------------------

def build_shape_mask(shape, W, H, margin_px, feather_px, out_label="[mask]"):
    """
    Grayscale mask (white=inside). Larger 'margin_px' => smaller shape.
    'feather_px' adds softening ONLY if requested; we’ll keep a hard copy for the border.
    """
    margin_px = int(round(margin_px))
    feather_px = max(0, int(round(feather_px)))

    if shape=="square":   expr=geq_rect_expr()
    elif shape=="circle": expr=geq_circle_expr()
    elif shape=="rhombus":expr=geq_rhombus_expr()
    elif shape=="triangle":expr=geq_triangle_expr()
    else: raise ValueError("Unsupported generated shape")

    seg  = f"color=c=black:s={W}x{H},format=gray[masksrc];"
    seg += f"[masksrc]geq=lum_expr='{expr}':cb_expr='128':cr_expr='128':alpha_expr='255',"
    seg  = seg.replace("margin", str(margin_px))
    if feather_px>0:
        sigma = max(0.1, feather_px/2.0)
        seg += f"gblur=sigma={sigma},"
    seg += f"format=gray{out_label};"
    return seg

def expand_mask_outward(hard_label, pixels, out_label):
    """
    Expand a HARD (binary) grayscale mask outward by ~`pixels`.
    We approximate dilation by blur -> threshold so it works on all builds.
    """
    # Use sigma ≈ pixels; then threshold low so the blur “turns on” new outer pixels.
    sigma = max(0.1, float(pixels))
    return (
        f"{hard_label}gblur=sigma={sigma},"
        f"lut='if(gt(val,16),255,0)',format=gray{out_label};"
    )

def ring_from_outer_minus_inner(outer_label, inner_label, out_label):
    """Make a ring by subtracting the inner mask from the expanded outer mask."""
    return f"{outer_label}{inner_label}blend=all_mode=difference,format=gray{out_label};"

def solid_rgba_with_alpha_from_mask(W, H, r, g, b, a255, mask_label, out_label):
    """Make a solid RGB frame and inject mask as its alpha."""
    a = max(0, min(255, a255)) / 255.0
    seg  = f"color=c=0x{r:02X}{g:02X}{b:02X}@{a}:s={W}x{H}[solid_{out_label[1:-1]}];"
    seg += f"[solid_{out_label[1:-1]}]{mask_label}alphamerge{out_label};"
    return seg

# --------------------- main builder ---------------------

def build_ffmpeg_cmd(bg, pip, out, position="tr", pad=24,
                     pip_percent=30.0, pip_width=None, pip_height=None,
                     shape="square", mask_path=None,
                     feather_px=16,                       # for PiP edge ONLY
                     border_px=6, border_color="#FFFFFF", # independent border
                     pip_opacity=1.0, rotate_deg=0.0,
                     crf=18, preset="veryfast", audio="bg"):
    need("ffmpeg")
    if not os.path.isfile(bg):  sys.exit(f"❌ Background not found: {bg}")
    if not os.path.isfile(pip): sys.exit(f"❌ PiP not found: {pip}")
    if shape=="mask" and not mask_path: sys.exit("❌ shape=mask requires --mask")

    bg_w, bg_h = ffprobe_dims(bg)
    src_w, src_h = ffprobe_dims(pip)

    # ---- target size ----
    if pip_width or pip_height:
        if pip_width and pip_height:
            tw,th = pip_width, pip_height
        elif pip_width:
            tw = pip_width
            th = int(round(tw * src_h/src_w))
        else:
            th = pip_height
            tw = int(round(th * src_w/src_h))
    else:
        scale = max(0.01, pip_percent/100.0)
        tw = int(round(bg_w * scale))
        th = int(round(tw * src_h/src_w))
        if th>bg_h:
            th = bg_h
            tw = int(round(th * src_w/src_h))

    # ---- positions ----
    positions = {
        "tr": (f"W-w-{pad}", f"{pad}"),
        "tl": (f"{pad}",     f"{pad}"),
        "br": (f"W-w-{pad}", f"H-h-{pad}"),
        "bl": (f"{pad}",     f"H-h-{pad}"),
        "c":  ("(W-w)/2",    "(H-h)/2"),
    }
    if position not in positions:
        sys.exit("❌ Invalid --pos")
    ox, oy = positions[position]

    # ---- color and opacity ----
    r,g,b,a = parse_hex_rgba(border_color, default_alpha=255)
    pip_opacity = max(0.0, min(1.0, float(pip_opacity)))
    border_px = max(0, int(round(border_px)))
    feather_px = max(0, int(round(feather_px)))

    # ---- inputs ----
    inputs = ["-y", "-i", bg, "-i", pip]
    if shape=="mask":
        inputs += ["-i", mask_path]

    # ---- PiP scaling & rotation ----
    pre = f"[1:v]scale={tw}:{th}:flags=bicubic"
    if rotate_deg:
        pre += f",rotate={math.radians(rotate_deg)}:ow=iw:oh=ih:c=black@0"
    pre += "[p];"

    # ---- Build two masks: HARD (binary) and SOFT (feathered) ----
    if shape=="mask":
        # External grayscale mask → hard binary, then an optional soft copy for feather
        mhard  = f"[2:v]format=gray,scale={tw}:{th}:flags=area,lut='if(gt(val,16),255,0)',format=gray[mhard];"
        if feather_px>0:
            sigma = max(0.1, feather_px/2.0)
            msoft = f"[mhard]gblur=sigma={sigma},format=gray[msoft];"
        else:
            msoft = "[mhard]copy[msoft];"
        mask_hard_label = "[mhard]"
        mask_soft_label = "[msoft]"
    else:
        # Generated shape: hard has NO blur; soft gets feather if requested
        base_margin = 0  # decouple from feather entirely
        mhard  = build_shape_mask(shape, tw, th, base_margin, 0, out_label="[mhard]")
        if feather_px>0:
            sigma = max(0.1, feather_px/2.0)
            msoft = f"[mhard]gblur=sigma={sigma},format=gray[msoft];"
        else:
            msoft = "[mhard]copy[msoft];"
        mask_hard_label = "[mhard]"
        mask_soft_label = "[msoft]"

    # ---- Apply SOFT mask as PiP alpha (for feathered edge only) ----
    comp_pip  = "[p]format=rgba[p_rgba0];"
    comp_pip += f"{mask_soft_label}format=gray[am];"
    comp_pip += "[p_rgba0][am]alphamerge[p_rgba1];"
    if pip_opacity < 1.0:
        comp_pip += f"[p_rgba1]colorchannelmixer=aa={pip_opacity}[p_rgba];"
    else:
        comp_pip += f"[p_rgba1]copy[p_rgba];"

    # ---- BORDER: expand HARD mask outward by border_px, ring = outer - hard ----
    border_graph = ""
    border_rgba_label = None
    if border_px > 0:
        # outer ≈ dilated(mhard, border_px) via blur→threshold
        border_graph += expand_mask_outward(mask_hard_label, border_px, "[mouter]")
        # ring = outer - hard
        border_graph += ring_from_outer_minus_inner("[mouter]", mask_hard_label, "[ring]")
        # colorize ring (RGBA with the ring as alpha)
        border_graph += solid_rgba_with_alpha_from_mask(tw, th, r, g, b, a, "[ring]", "[border_rgba]")
        border_rgba_label = "[border_rgba]"

    # ---- Compose: PiP first, then BORDER ON TOP (independent of feather) ----
    graph  = pre
    graph += mhard
    graph += msoft
    graph += comp_pip
    graph += f"[0:v][p_rgba]overlay=x={ox}:y={oy}:format=auto[bg1];"
    graph += border_graph
    if border_rgba_label:
        graph += f"[bg1]{border_rgba_label}overlay=x={ox}:y={oy}:format=auto[outv]"
    else:
        graph += f"[bg1]copy[outv]"

    # ---- audio mapping ----
    map_audio=[]
    # For 'mix', amix needs both streams; if one is missing, recommend bg/pip
    if audio=="bg":
        map_audio=["-map","0:a?"]
    elif audio=="pip":
        map_audio=["-map","1:a?"]
    elif audio=="mix":
        graph += ";[0:a][1:a]amix=inputs=2:dropout_transition=0:normalize=0[outa]"
        map_audio=["-map","[outa]"]
    elif audio=="none":
        map_audio=[]

    cmd = ["ffmpeg"] + inputs + [
        "-filter_complex", graph,
        "-map","[outv]"
    ] + map_audio + [
        "-c:v","libx264","-pix_fmt","yuv420p",
        "-movflags","+faststart",
        "-crf",str(crf), "-preset", preset,
        "-shortest",
        out
    ]
    return cmd

# --------------------- CLI ---------------------

def main():
    p=argparse.ArgumentParser(description="PiP with independent border (decoupled from feather), optional feathered PiP edge, rotation, and audio.")
    p.add_argument("-i","--input",required=True)
    p.add_argument("-p","--pip",required=True)
    p.add_argument("-o","--output",required=True)

    p.add_argument("--pos",default="tr",choices=["tl","tr","bl","br","c"])
    p.add_argument("--pad",type=int,default=24)

    g=p.add_argument_group("Size")
    g.add_argument("--pip-percent",type=float,default=30.0)
    g.add_argument("--pip-width",type=int)
    g.add_argument("--pip-height",type=int)

    s=p.add_argument_group("Shape")
    s.add_argument("--shape",default="square",choices=["square","circle","triangle","rhombus","mask"])
    s.add_argument("--mask",help="External mask (white=opaque) if --shape mask")

    o=p.add_argument_group("Look")
    o.add_argument("--feather",type=int,default=0,help="PiP edge softness ONLY (0 keeps a hard edge).")
    o.add_argument("--pip-opacity",type=float,default=1.0,help="0..1")
    o.add_argument("--rotate",type=float,default=0.0,help="degrees")

    b=p.add_argument_group("Border")
    b.add_argument("--border-width",type=int,default=6,help="Visible even when feather=0; grows outward.")
    b.add_argument("--border-color",default="#FFFFFF",help="#RRGGBB[AA] or CSS name (e.g., red)")

    e=p.add_argument_group("Encode")
    e.add_argument("--crf",type=int,default=18)
    e.add_argument("--preset",default="veryfast",choices=["ultrafast","superfast","veryfast","faster","fast","medium","slow","slower","veryslow"])
    e=p.add_argument_group("Audio")
    e.add_argument("--audio",default="bg",choices=["bg","pip","mix","none"])

    a=p.parse_args()

    cmd = build_ffmpeg_cmd(
        bg=a.input, pip=a.pip, out=a.output,
        position=a.pos, pad=a.pad,
        pip_percent=a.pip_percent, pip_width=a.pip_width, pip_height=a.pip_height,
        shape=a.shape, mask_path=a.mask,
        feather_px=a.feather,
        border_px=a.border_width, border_color=a.border_color,
        pip_opacity=a.pip_opacity, rotate_deg=a.rotate,
        crf=a.crf, preset=a.preset, audio=a.audio
    )
    print("▶️ FFmpeg:\n", " ".join([subprocess.list2cmdline([c]) if " " in c else c for c in cmd]), "\n")
    r = subprocess.run(cmd)
    if r.returncode != 0:
        sys.exit(f"❌ FFmpeg failed with code {r.returncode}")
    print(f"✅ Done: {a.output}")

if __name__=="__main__":
    main()
