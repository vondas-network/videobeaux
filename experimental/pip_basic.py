#!/usr/bin/env python3
import argparse, os, re, subprocess, sys, math
from shutil import which

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

# ---- Shape masks via geq ----
def geq_rect_expr():
    return "if(between(X,margin,W-1-margin)*between(Y,margin,H-1-margin),255,0)"
def geq_circle_expr():
    return "if(lte(hypot(X-W/2,Y-H/2),min(W,H)/2-margin),255,0)"
def geq_rhombus_expr():
    return ("if(lte("
            "(abs(X-W/2)/max(W/2-margin,1)) + (abs(Y-H/2)/max(H/2-margin,1))"
            ",1),255,0)")
def geq_triangle_expr():
    return "if( (gte(Y/H, 2*abs(X/W-0.5) + margin/H)) * (lte(Y/H, 1 - margin/H)), 255, 0)"

def build_shape_mask(shape, W, H, margin_px, feather_px, out_label="[mask]"):
    margin_px=max(0, int(round(margin_px)))
    feather_px=max(0, int(round(feather_px)))
    if shape=="square":   expr=geq_rect_expr()
    elif shape=="circle": expr=geq_circle_expr()
    elif shape=="rhombus":expr=geq_rhombus_expr()
    elif shape=="triangle":expr=geq_triangle_expr()
    else: raise ValueError("Unsupported generated shape")
    seg =  f"color=c=black:s={W}x{H},format=gray[masksrc];"
    seg += f"[masksrc]geq=lum_expr='{expr}':cb_expr='128':cr_expr='128':alpha_expr='255',"
    seg  = seg.replace("margin", str(margin_px))
    if feather_px>0:
        sigma=max(0.1, feather_px/2.0)
        seg += f"gblur=sigma={sigma},"
    seg += f"format=gray{out_label};"
    return seg

def build_border_ring(shape, W, H, base_margin, border_px):
    if border_px<=0: return "", None
    base = shape if shape in {"square","circle","triangle","rhombus"} else "square"
    outer = build_shape_mask(base, W,H, base_margin, 0, out_label="[outer]")
    inner = build_shape_mask(base, W,H, base_margin+border_px, 0, out_label="[inner]")
    ring  = "[outer][inner]blend=all_mode=difference,format=gray[ring];"
    return outer+inner+ring, "[ring]"

def build_ffmpeg_cmd(bg, pip, out, position="tr", pad=24,
                     pip_percent=30.0, pip_width=None, pip_height=None,
                     shape="square", mask_path=None, feather_px=16,
                     border_px=6, border_color="#FFFFFF",
                     pip_opacity=1.0,
                     rotate_deg=0.0,
                     crf=18, preset="veryfast", audio="bg"):
    need("ffmpeg")
    if not os.path.isfile(bg):  sys.exit(f"❌ Background not found: {bg}")
    if not os.path.isfile(pip): sys.exit(f"❌ PiP not found: {pip}")
    if shape=="mask" and not mask_path: sys.exit("❌ shape=mask requires --mask")

    bg_w,bg_h = ffprobe_dims(bg)
    src_w,src_h = ffprobe_dims(pip)

    # ---- target size ----
    if pip_width and pip_height:
        tw,th = int(pip_width), int(pip_height)
    elif pip_width:
        tw = int(pip_width); th = int(round(src_h*(tw/src_w)))
    elif pip_height:
        th = int(pip_height); tw = int(round(src_w*(th/src_h)))
    else:
        tw = int(round(bg_w * float(pip_percent)/100.0))
        th = int(round(src_h * (tw/src_w)))
    # clamp and force even
    tw = max(32, min(bg_w, tw)) & ~1
    th = max(32, min(bg_h, th)) & ~1

    # build inputs
    inputs = ["-y","-i",bg,"-i",pip]
    parts = []

    # ---- mask (always tw x th) ----
    margin = max(0,int(round(feather_px)))
    if shape=="mask":
        inputs += ["-loop","1","-i",mask_path]
        parts.append(f"[2:v]scale={tw}:{th},setsar=1,format=gray[mask];")
    else:
        parts.append(build_shape_mask(shape, tw, th, margin, feather_px, out_label="[mask]"))

    # ---- optional border ring ----
    ring_chain, ring_label = build_border_ring(shape, tw, th, margin, border_px)
    if ring_chain: parts.append(ring_chain)

    # ---- normalize PiP to target box ----
    parts.append(f"[1:v]scale={tw}:{th}:flags=lanczos,setsar=1[p0];")
    cur = "[p0]"

    # ---- rotation only (no flip/mirror) ----
    if abs(rotate_deg)>1e-6:
        ang = rotate_deg*math.pi/180.0
        parts.append(f"{cur}rotate={ang:.10f}:ow=iw:oh=ih:fillcolor=black@0,format=yuv444p[p1];")
        cur="[p1]"

    # ---- ensure EXACT target size right before alpha ----
    parts.append(f"{cur}scale={tw}:{th}:flags=bicubic,setsar=1[p_final];")
    cur="[p_final]"

    # ---- apply alpha mask ----
    parts.append(f"{cur}[mask]alphamerge[p_rgba];")

    # ---- overall PiP opacity ----
    if pip_opacity<1.0:
        a=clamp(pip_opacity,0.0,1.0)
        parts.append(f"[p_rgba]format=rgba,colorchannelmixer=aa={a:.6g}[p_rgba];")

    # ---- border underlay ----
    if ring_label:
        col = parse_rgba(border_color,1.0)
        parts.append(f"color=c={col}:s={tw}x{th}:r=30,format=rgba[border_col];")
        parts.append(f"[border_col]{ring_label}alphamerge[border_rgba];")

    ox,oy = build_position_expr(position,pad)

    graph="".join(parts)
    if ring_label:
        graph += f"[0:v][border_rgba]overlay=x={ox}:y={oy}[bg1];"
        base="[bg1]"
    else:
        base="[0:v]"
    graph += f"{base}[p_rgba]overlay=x={ox}:y={oy}:format=auto:eval=frame[outv]"

    # ---- audio ----
    map_audio=[]
    if audio=="bg":   map_audio=["-map","0:a?"]
    elif audio=="pip":map_audio=["-map","1:a?"]
    elif audio=="mix":
        graph += ";[0:a][1:a]amix=inputs=2:dropout_transition=0:normalize=0[outa]"
        map_audio=["-map","[outa]"]
    elif audio=="none": map_audio=[]

    cmd=["ffmpeg"]+inputs+[
        "-filter_complex", graph,
        "-map","[outv]"
    ]+map_audio+[
        "-c:v","libx264",
        "-pix_fmt","yuv420p",
        "-profile:v","high",
        "-level:v","4.1",
        "-movflags","+faststart",
        "-color_primaries","bt709",
        "-color_trc","bt709",
        "-colorspace","bt709",
        "-crf",str(crf),
        "-preset",preset,
        "-shortest",
        out
    ]
    return cmd

def main():
    p=argparse.ArgumentParser(description="Robust FFmpeg PiP (NO flip/mirror): shapes, feathered mask, border, rotation, preview-safe output.")
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
    s.add_argument("--mask",help="External mask path for shape=mask (white=opaque, black=transparent)")
    s.add_argument("--feather",type=int,default=16,help="Feather width along edges (mask blur)")

    b=p.add_argument_group("Border")
    b.add_argument("--border-width",type=int,default=6)
    b.add_argument("--border-color",default="#FFFFFF")

    t=p.add_argument_group("Transform")
    t.add_argument("--rotate",type=float,default=0.0,help="Degrees clockwise (only transform enabled)")

    e=p.add_argument_group("Encode")
    e.add_argument("--crf",type=int,default=18)
    e.add_argument("--preset",default="veryfast")
    p.add_argument("--pip-opacity",type=float,default=1.0)
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
        crf=a.crf, preset=a.preset, audio=a.audio
    )
    print("▶️ FFmpeg:\n", " ".join([subprocess.list2cmdline([c]) if " " in c else c for c in cmd]), "\n")
    r=subprocess.run(cmd)
    if r.returncode!=0: sys.exit(f"❌ FFmpeg failed with code {r.returncode}")
    print(f"✅ Done: {a.output}")

if __name__=="__main__":
    main()
