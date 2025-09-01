#!/usr/bin/env python3
"""
Lumask — PNG-only generative mask/stencil tool
Symmetry:
  --mirror none|horizontal|vertical|both
  --diag-mirror none|diag|antidiag|both
  --radial-sym N
  --dihedral N
  --grid CxR (or a single integer -> NxN), --grid-spacing S (fraction of min(W,H))
  --spiral K, --spiral-rot-deg D, --spiral-scale S

Other:
  Transparent mask (--mode mask) or color preview (--mode color, --bg)
  Noise placement (perlin/value)
  Frame-safe sizing (no giant whiteouts), keep-in-frame clamping
  Batch generation → timestamped folder + filenames + PNG metadata
"""

import argparse
import json
import math
import os
import random
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple, Optional
from PIL import Image, ImageDraw, ImageColor, PngImagePlugin

# -----------------------------
# Constants / Presets
# -----------------------------
TWO_PI = math.pi * 2
SHAPES = [
    "circle", "square", "triangle", "vertical", "horizontal",
    "diagonal", "diagonal-flipped", "polygon", "rhombus",
    "octagon", "pentagon", "nonagon"
]

PRESETS = {
    "sd": (320, 240),
    "720hd": (640, 360),
    "1080hd": (960, 540),
    "widescreen": (320, 180),
    "portrait1080": (1080, 1620),
}

# -----------------------------
# Data classes
# -----------------------------
@dataclass
class PlaneParams:
    shape: str
    size: float
    x: float
    y: float
    rotation: float
    stretchX: float
    stretchY: float
    alpha: int = 255

@dataclass
class GenConfig:
    W: int
    H: int
    mode: str
    bg_hex: str
    planes: int
    no_rand: bool
    seed: int
    noise_mode: str
    noise_scale: float
    noise_strength: float
    # symmetry
    mirror: str          # none|horizontal|vertical|both
    diag_mirror: str     # none|diag|antidiag|both
    radial_sym: int
    dihedral: int        # >=2 enables D_n
    grid_cols: int
    grid_rows: int
    grid_spacing: float  # fraction of min(W,H)
    spiral_k: int
    spiral_rot_deg: float
    spiral_scale: float
    # sizing / safety
    size_min: float
    size_max: float
    margin: float
    fit_enabled: bool
    keep_in_frame: bool

# -----------------------------
# Utilities
# -----------------------------
def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

def rng_pick(rng: random.Random, items: List[str]) -> str:
    return items[rng.randrange(0, len(items))]

def hex_to_rgba(hex_str: str, alpha: int = 255) -> Tuple[int, int, int, int]:
    c = ImageColor.getrgb(hex_str)
    return (c[0], c[1], c[2], alpha)

def polygon_points(cx: float, cy: float, radius: float, n: int) -> List[Tuple[float, float]]:
    return [(cx + math.cos(i * (TWO_PI / n)) * radius,
             cy + math.sin(i * (TWO_PI / n)) * radius) for i in range(n)]

def paste_centered(base: Image.Image, layer: Image.Image, cx: float, cy: float) -> None:
    x = int(round(cx - layer.width / 2))
    y = int(round(cy - layer.height / 2))
    base.alpha_composite(layer, (x, y))

def format_outname(base_path: str, preset: str, idx: Optional[int], digits: int, ts: Optional[str] = None) -> str:
    root, ext = os.path.splitext(base_path)
    parts = [root]
    if preset:
        parts.append(preset)
    if idx is not None:
        parts.append(str(idx).zfill(digits))
    if ts:
        parts.append(ts)
    return os.path.abspath(f"{'_'.join(parts)}{ext}")

# -----------------------------
# Noise (value + Perlin)
# -----------------------------
def hash2d(xi: int, yi: int, seed: int) -> float:
    n = (xi * 374761393 + yi * 668265263) ^ (seed * 1274126177)
    n = (n ^ (n >> 13)) * 1274126177
    n = (n ^ (n >> 16)) & 0xFFFFFFFF
    return n / 0x100000000

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def smoothstep(t: float) -> float:
    return t * t * (3 - 2 * t)

def value_noise(x: float, y: float, seed: int) -> float:
    xi, yi = math.floor(x), math.floor(y)
    xf, yf = x - xi, y - yi
    v00 = hash2d(xi, yi, seed)
    v10 = hash2d(xi + 1, yi, seed)
    v01 = hash2d(xi, yi + 1, seed)
    v11 = hash2d(xi + 1, yi + 1, seed)
    u = smoothstep(xf)
    v = smoothstep(yf)
    return lerp(lerp(v00, v10, u), lerp(v01, v11, u), v)

def grad(hashv: int, x: float, y: float) -> float:
    h = hashv & 7
    u = x if h < 4 else y
    v = y if h < 4 else x
    return ((u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v))

def perlin(x: float, y: float, seed: int) -> float:
    xi, yi = math.floor(x), math.floor(y)
    xf, yf = x - xi, y - yi
    h00 = int(hash2d(xi, yi, seed) * 256)
    h10 = int(hash2d(xi + 1, yi, seed) * 256)
    h01 = int(hash2d(xi, yi + 1, seed) * 256)
    h11 = int(hash2d(xi + 1, yi + 1, seed) * 256)
    u = smoothstep(xf)
    v = smoothstep(yf)
    n00 = grad(h00, xf, yf)
    n10 = grad(h10, xf - 1, yf)
    n01 = grad(h01, xf, yf - 1)
    n11 = grad(h11, xf - 1, yf - 1)
    nx0 = lerp(n00, n10, u)
    nx1 = lerp(n01, n11, u)
    return (lerp(nx0, nx1, v) + 1) * 0.5

def sample_noise(nx: float, ny: float, seed: int, mode: str) -> float:
    if mode == "perlin":
        return perlin(nx, ny, seed)
    elif mode == "value":
        return value_noise(nx, ny, seed)
    return 0.5

# -----------------------------
# Frame-safe helpers
# -----------------------------
def rotated_bbox(w: float, h: float, theta: float) -> Tuple[float, float]:
    ct = abs(math.cos(theta))
    st = abs(math.sin(theta))
    return (w * ct + h * st, w * st + h * ct)

def fit_size_to_canvas(size: float, stretchX: float, stretchY: float, rotation: float,
                       W: int, H: int, margin: float) -> float:
    w = size * stretchX
    h = size * stretchY
    bw, bh = rotated_bbox(w, h, rotation)
    maxW = W * margin
    maxH = H * margin
    scale = min(1.0, maxW / bw if bw > 0 else 1.0, maxH / bh if bh > 0 else 1.0)
    return size * scale

def clamp_position_to_canvas(x: float, y: float, size: float, stretchX: float, stretchY: float,
                             rotation: float, W: int, H: int, margin: float) -> Tuple[float, float]:
    w = size * stretchX
    h = size * stretchY
    bw, bh = rotated_bbox(w, h, rotation)
    halfW = (W * margin - bw) / 2.0
    halfH = (H * margin - bh) / 2.0
    if halfW < 0: halfW = 0
    if halfH < 0: halfH = 0
    return (max(-halfW, min(halfW, x)), max(-halfH, min(halfH, y)))

# -----------------------------
# Param generation & noise
# -----------------------------
def generate_params(rng: random.Random, width: int, height: int, planes: int, do_randomize: bool,
                    size_min: float, size_max: float) -> List[PlaneParams]:
    out: List[PlaneParams] = []
    base = min(width, height)
    min_px = max(2.0, base * size_min)
    max_px = max(min_px + 1.0, base * size_max)
    for i in range(planes):
        shape = rng_pick(rng, SHAPES) if do_randomize else SHAPES[i % len(SHAPES)]
        size = rng.uniform(min_px, max_px) if do_randomize else (0.5 * (min_px + max_px))
        x = rng.uniform(-width / 2, width / 2) if do_randomize else 0.0
        y = rng.uniform(-height / 2, height / 2) if do_randomize else 0.0
        rot = rng.uniform(0, TWO_PI) if do_randomize else 0.0
        sx = rng.uniform(0.5, 2.0) if do_randomize else 1.0
        sy = rng.uniform(0.5, 2.0) if do_randomize else 1.0
        out.append(PlaneParams(shape, size, x, y, rot, sx, sy, 255))
    return out

def apply_noise_to_params(params: List[PlaneParams], cfg: GenConfig) -> None:
    if cfg.noise_mode == "none" or cfg.noise_strength <= 0 or cfg.noise_scale <= 0:
        return
    W, H = cfg.W, cfg.H
    for idx, p in enumerate(params):
        nx = (p.x + W * 0.5) * cfg.noise_scale
        ny = (p.y + H * 0.5) * cfg.noise_scale
        n1 = sample_noise(nx + 10.123 * idx, ny + 20.456 * idx, cfg.seed, cfg.noise_mode)
        n2 = sample_noise(nx + 33.789 * idx, ny + 44.012 * idx, cfg.seed ^ 0xABCDEF, cfg.noise_mode)
        p.x += (n1 - 0.5) * (W * cfg.noise_strength)
        p.y += (n2 - 0.5) * (H * cfg.noise_strength)
        n3 = sample_noise(nx - 55.5, ny + 66.6, cfg.seed ^ 0x123456, cfg.noise_mode)
        p.rotation += (n3 - 0.5) * 0.25

def enforce_frame_safety(params: List[PlaneParams], cfg: GenConfig) -> None:
    for p in params:
        if cfg.fit_enabled:
            p.size = fit_size_to_canvas(p.size, p.stretchX, p.stretchY, p.rotation, cfg.W, cfg.H, cfg.margin)
        if cfg.keep_in_frame:
            p.x, p.y = clamp_position_to_canvas(p.x, p.y, p.size, p.stretchX, p.stretchY, p.rotation,
                                                cfg.W, cfg.H, cfg.margin)

# -----------------------------
# Symmetry helpers
# -----------------------------
def rotate_vec(x: float, y: float, ang: float) -> Tuple[float, float]:
    ca, sa = math.cos(ang), math.sin(ang)
    return (x * ca - y * sa, x * sa + y * ca)

def add_mirror_variants(x: float, y: float, rot: float, mirror: str) -> List[Tuple[float, float, float]]:
    out = [(x, y, rot)]
    if mirror in ("horizontal", "both"):
        out.append((-x, y, -rot))
    if mirror in ("vertical", "both"):
        out.append((x, -y, -rot))
    if mirror == "both":
        out.append((-x, -y, rot))
    return out

def add_diag_mirror_variants(x: float, y: float, rot: float, diag_mirror: str) -> List[Tuple[float, float, float]]:
    out = [(x, y, rot)]
    if diag_mirror in ("diag", "both"):
        out.append(( y,  x, (math.pi/2) - rot))
    if diag_mirror in ("antidiag", "both"):
        out.append((-y, -x, -(math.pi/2) - rot))
    return out

def add_dihedral_variants(x: float, y: float, rot: float, n: int) -> List[Tuple[float, float, float]]:
    """
    Dihedral D_n: for each sector k, add a rotated copy and its mirror.
    Construct by taking base {(x,y,rot), (x,-y,-rot)} and rotating by 2πk/n.
    """
    if n is None or n < 2:
        return [(x, y, rot)]
    base = [(x, y, rot), (x, -y, -rot)]
    out: List[Tuple[float, float, float]] = []
    for k in range(n):
        a = (k / n) * TWO_PI
        for px, py, pr in base:
            rx, ry = rotate_vec(px, py, a)
            out.append((rx, ry, pr + a))
    return out

def parse_grid_spec(spec: Optional[str]) -> Tuple[int, int]:
    if not spec:
        return (0, 0)
    s = spec.lower().replace(" ", "")
    if "x" in s:
        c, r = s.split("x", 1)
        try:
            return (max(1, int(c)), max(1, int(r)))
        except:
            return (0, 0)
    try:
        n = int(s)
        side = max(1, int(round(math.sqrt(n))))
        return (side, side)
    except:
        return (0, 0)

def add_grid_variants(x: float, y: float, rot: float, cols: int, rows: int,
                      spacing: float, W: int, H: int) -> List[Tuple[float, float, float]]:
    """Place copies on a centered CxR grid. spacing is fraction of min(W,H) between cell centers."""
    if cols < 1 or rows < 1:
        return [(x, y, rot)]
    out: List[Tuple[float, float, float]] = []
    base_step = max(1.0, min(W, H) * spacing)
    x0 = - (cols - 1) * 0.5 * base_step
    y0 = - (rows - 1) * 0.5 * base_step
    for ci in range(cols):
        for ri in range(rows):
            gx = x + x0 + ci * base_step
            gy = y + y0 + ri * base_step
            out.append((gx, gy, rot))
    return out

def add_spiral_variants(x: float, y: float, rot: float, k: int, rot_deg: float, scale: float) -> List[Tuple[float, float, float]]:
    """Create k-1 additional copies along a spiral (position rotated and radius multiplied)."""
    if k is None or k < 2:
        return [(x, y, rot)]
    out = [(x, y, rot)]
    step = math.radians(rot_deg)
    r0 = math.hypot(x, y)
    theta0 = math.atan2(y, x)
    for i in range(1, k):
        r = r0 * (scale ** i)
        theta = theta0 + step * i
        sx = r * math.cos(theta)
        sy = r * math.sin(theta)
        srot = rot + step * i
        out.append((sx, sy, srot))
    return out

# -----------------------------
# Drawing
# -----------------------------
def draw_base_shape(shape: str, size: int, fill: Tuple[int, int, int, int]) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size
    if shape == "circle":
        d.ellipse([0, 0, s, s], fill=fill)
    elif shape == "square":
        d.rectangle([0, 0, s, s], fill=fill)
    elif shape == "triangle":
        h = s * (math.sqrt(3) / 2)
        pts = [(s * 0.0, s * 0.5 + h / 6),
               (s * 1.0, s * 0.5 + h / 6),
               (s * 0.5, s * 0.5 - 2 * h / 6)]
        d.polygon(pts, fill=fill)
    elif shape == "vertical":
        d.rectangle([s * 0.375, 0, s * 0.625, s], fill=fill)
    elif shape == "horizontal":
        d.rectangle([0, s * 0.375, s, s * 0.625], fill=fill)
    elif shape in ("diagonal", "diagonal-flipped"):
        d.rectangle([0, s * 0.375, s, s * 0.625], fill=fill)
        img = img.rotate(45 if shape == "diagonal" else -45, resample=Image.BICUBIC, expand=True)
    elif shape == "polygon":
        d.polygon(polygon_points(s / 2, s / 2, s / 2, 6), fill=fill)
    elif shape == "rhombus":
        d.polygon([(s * 0.5, 0), (s, s * 0.5), (s * 0.5, s), (0, s * 0.5)], fill=fill)
    elif shape == "octagon":
        d.polygon(polygon_points(s / 2, s / 2, s / 2, 8), fill=fill)
    elif shape == "pentagon":
        d.polygon(polygon_points(s / 2, s / 2, s / 2, 5), fill=fill)
    elif shape == "nonagon":
        d.polygon(polygon_points(s / 2, s / 2, s / 2, 9), fill=fill)
    else:
        d.ellipse([0, 0, s, s], fill=fill)
    return img

def draw_planes_to_png(params: List[PlaneParams], cfg: GenConfig, out_path: str, timestamp: Optional[str]) -> None:
    if cfg.mode == "mask":
        base = Image.new("RGBA", (cfg.W, cfg.H), (0, 0, 0, 0))
        shape_fill = (255, 255, 255, 255)
    else:
        base = Image.new("RGBA", (cfg.W, cfg.H), hex_to_rgba(cfg.bg_hex, 255))
        shape_fill = (190, 190, 190, 255)

    def draw_one_at(xc: float, yc: float, rot: float, sx: float, sy: float, shape: str, size: float):
        s = max(2, int(round(size)))
        shape_img = draw_base_shape(shape, s, shape_fill)
        sw = max(1, int(round(shape_img.width * sx)))
        sh = max(1, int(round(shape_img.height * sy)))
        if (sw, sh) != shape_img.size:
            shape_img = shape_img.resize((sw, sh), resample=Image.LANCZOS)
        deg = math.degrees(rot)
        if abs(deg) > 0.0001:
            shape_img = shape_img.rotate(deg, resample=Image.BICUBIC, expand=True)
        paste_centered(base, shape_img, xc, yc)

    cx, cy = cfg.W / 2, cfg.H / 2
    for p in params:
        # Compose symmetries in stages:

        # 1) Axis mirrors
        axis_set = add_mirror_variants(p.x, p.y, p.rotation, cfg.mirror)

        # 2) Diagonal mirrors
        diag_set: List[Tuple[float, float, float]] = []
        for axx, axy, arot in axis_set:
            diag_set.extend(add_diag_mirror_variants(axx, axy, arot, cfg.diag_mirror))

        # 3) Dihedral (kaleidoscope) around center
        dih_set: List[Tuple[float, float, float]] = []
        for dx, dy, drot in diag_set:
            dih_set.extend(add_dihedral_variants(dx, dy, drot, cfg.dihedral))

        # 4) Grid (translate to lattice positions)
        grid_set: List[Tuple[float, float, float]] = []
        for gx, gy, grot in dih_set:
            grid_set.extend(add_grid_variants(gx, gy, grot, cfg.grid_cols, cfg.grid_rows, cfg.grid_spacing, cfg.W, cfg.H))

        # 5) Spiral (successive rotate & radius scale)
        spiral_set: List[Tuple[float, float, float]] = []
        for qx, qy, qrot in grid_set:
            spiral_set.extend(add_spiral_variants(qx, qy, qrot, cfg.spiral_k, cfg.spiral_rot_deg, cfg.spiral_scale))

        # 6) Base + radial symmetry copies
        for bx, by, brot in spiral_set:
            # base
            draw_one_at(cx + bx, cy + by, brot, p.stretchX, p.stretchY, p.shape, p.size)
            # radial copies
            if cfg.radial_sym and cfg.radial_sym > 1:
                for k in range(cfg.radial_sym):
                    ang = (k / cfg.radial_sym) * TWO_PI
                    rx, ry = rotate_vec(bx, by, ang)
                    draw_one_at(cx + rx, cy + ry, brot + ang, p.stretchX, p.stretchY, p.shape, p.size)

    pnginfo = PngImagePlugin.PngInfo()
    if timestamp:
        pnginfo.add_text("lumask_timestamp", timestamp)
    pnginfo.add_text("lumask_seed", str(cfg.seed))
    pnginfo.add_text("lumask_mode", cfg.mode)
    base.save(out_path, "PNG", pnginfo=pnginfo)

# -----------------------------
# Orchestration (one / batch)
# -----------------------------
def generate_one(seed_val: int, W: int, H: int, args: argparse.Namespace,
                 preset: str, idx: Optional[int], digits: int,
                 out_dir: Optional[str] = None, ts: Optional[str] = None) -> None:
    rng = random.Random(seed_val)
    params = generate_params(
        rng, W, H, args.planes, not args.no_rand,
        size_min=args.size_min, size_max=args.size_max
    )

    grid_cols, grid_rows = parse_grid_spec(args.grid)

    cfg = GenConfig(
        W=W, H=H, mode=args.mode, bg_hex=args.bg, planes=args.planes,
        no_rand=args.no_rand, seed=seed_val,
        noise_mode=args.noise, noise_scale=args.noise_scale, noise_strength=args.noise_strength,
        mirror=args.mirror, diag_mirror=args.diag_mirror, radial_sym=args.radial_sym or 0,
        dihedral=args.dihedral or 0,
        grid_cols=grid_cols, grid_rows=grid_rows, grid_spacing=args.grid_spacing,
        spiral_k=args.spiral or 0, spiral_rot_deg=args.spiral_rot_deg, spiral_scale=args.spiral_scale,
        size_min=args.size_min, size_max=args.size_max,
        margin=args.margin, fit_enabled=(not args.no_fit), keep_in_frame=not args.no_keep_in_frame
    )

    # Noise + safety
    apply_noise_to_params(params, cfg)
    enforce_frame_safety(params, cfg)

    # Output names
    digits = max(digits, 2)
    ts_str = ts or now_stamp()

    def in_dir(path: str) -> str:
        return os.path.join(out_dir, os.path.basename(path)) if out_dir else path

    out_png = in_dir(format_outname(args.out, preset, idx, digits, ts_str))

    draw_planes_to_png(params, cfg, out_png, ts_str)
    print(f"[✓] Wrote {out_png}")

    if args.config:
        conf_path = in_dir(format_outname(args.config, preset, idx, digits, ts_str))
        conf = {
            "timestamp": ts_str,
            "seed": seed_val,
            "mode": args.mode,
            "bg": args.bg,
            "width": W,
            "height": H,
            "preset": preset,
            "planes": args.planes,
            "randomized": not args.no_rand,
            "noise": {
                "mode": args.noise,
                "scale": args.noise_scale,
                "strength": args.noise_strength
            },
            "symmetry": {
                "mirror": args.mirror,
                "diag_mirror": args.diag_mirror,
                "radial_sym": args.radial_sym or 0,
                "dihedral": args.dihedral or 0,
                "grid": {"spec": args.grid, "cols": grid_cols, "rows": grid_rows, "spacing_frac": args.grid_spacing},
                "spiral": {"k": args.spiral or 0, "rot_deg": args.spiral_rot_deg, "scale": args.spiral_scale}
            },
            "size": {
                "min_frac": args.size_min,
                "max_frac": args.size_max
            },
            "fit": {
                "enabled": not args.no_fit,
                "margin": args.margin,
                "keep_in_frame": not args.no_keep_in_frame
            },
            "params": [p.__dict__ for p in params],
        }
        with open(conf_path, "w", encoding="utf-8") as f:
            json.dump(conf, f, indent=2)
        print(f"[✓] Wrote {conf_path}")

    print(f"    seed={seed_val} mode={args.mode} size={W}x{H} planes={args.planes} preset={preset} noise={args.noise}")

def generate_batch(args: argparse.Namespace, W: int, H: int, preset: str) -> None:
    batch_ts = now_stamp()
    root, _ext = os.path.splitext(os.path.basename(args.out))
    batch_dir = f"{root}_{preset}_{batch_ts}_batch"
    os.makedirs(batch_dir, exist_ok=True)
    total = int(args.batch)
    digits = len(str(total))
    print(f"==> Batch: writing {total} file(s) to ./{batch_dir}")

    for i in range(1, total + 1):
        seed_val = random.randrange(1, 10**9) if (args.auto_seed or args.seed is None) else (args.seed + i - 1)
        print(f"[{i}/{total}] Generating (seed={seed_val}) …")
        generate_one(seed_val, W, H, args, preset, idx=i, digits=digits, out_dir=batch_dir, ts=batch_ts)

# -----------------------------
# CLI
# -----------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description="Lumask PNG generator (noise, rich symmetry, frame-safe sizing, batch folders).")
    ap.add_argument("--preset", default="portrait1080",
                    help="sd, 720hd, 1080hd, widescreen, portrait1080 (default)")
    ap.add_argument("--w", type=int, help="Custom width (overrides preset)")
    ap.add_argument("--h", type=int, help="Custom height (overrides preset)")
    ap.add_argument("--out", default="lumask.png",
                    help="Output base path (used to build batch folder + filenames)")
    ap.add_argument("--planes", type=int, default=3, help="Number of planes")
    ap.add_argument("--seed", type=int, help="Deterministic seed")
    ap.add_argument("--auto-seed", action="store_true", help="Ignore --seed and pick a fresh one each run")
    ap.add_argument("--batch", type=int, help="Generate N masks; creates a timestamped folder")

    ap.add_argument("--mode", choices=["mask", "color"], default="mask",
                    help="mask=transparent bg + white; color=solid bg + gray")
    ap.add_argument("--config", help="Write JSON config (suffix matches batch/preset/timestamp)")
    ap.add_argument("--no-rand", action="store_true", help="Disable randomization")
    ap.add_argument("--bg", default="#FFFFFF", help="Background color for color mode (hex)")

    # Noise
    ap.add_argument("--noise", choices=["none", "perlin", "value"], default="none", help="Noise source")
    ap.add_argument("--noise-scale", type=float, default=0.003, help="Noise frequency scale (smaller = smoother)")
    ap.add_argument("--noise-strength", type=float, default=0.0, help="Displacement strength as fraction of canvas (0..1)")

    # Symmetry (axis + diagonal + radial)
    ap.add_argument("--mirror", choices=["none", "horizontal", "vertical", "both"], default="none",
                    help="Axis mirroring")
    ap.add_argument("--diag-mirror", choices=["none", "diag", "antidiag", "both"], default="none",
                    help="Diagonal mirroring (diag=y=x, antidiag=y=-x)")
    ap.add_argument("--radial-sym", type=int, help="Number of radial symmetry copies (>=2)")

    # New symmetry systems
    ap.add_argument("--dihedral", type=int, help="Dihedral kaleidoscope sectors (>=2)")
    ap.add_argument("--grid", type=str, help="Grid copies as CxR (e.g., 3x2 or 4x4); integer -> NxN")
    ap.add_argument("--grid-spacing", type=float, default=0.6, help="Grid spacing as fraction of min(W,H) between cells")
    ap.add_argument("--spiral", type=int, help="Spiral copies (>=2)")
    ap.add_argument("--spiral-rot-deg", type=float, default=20.0, help="Spiral rotation per copy (degrees)")
    ap.add_argument("--spiral-scale", type=float, default=1.08, help="Spiral radius multiplier per copy")

    # Sizing & fitting controls
    ap.add_argument("--size-min", type=float, default=0.20, help="Min size as fraction of min(W,H) [0..1]")
    ap.add_argument("--size-max", type=float, default=0.65, help="Max size as fraction of min(W,H) [0..1]")
    ap.add_argument("--margin", type=float, default=0.95, help="Fit margin (1.0 = tight fit, 0.95 = 5% inset)")
    ap.add_argument("--no-fit", action="store_true", help="Disable fit-to-frame (allow overflow)")
    ap.add_argument("--no-keep-in-frame", action="store_true", help="Do not clamp positions to keep bbox inside")

    args = ap.parse_args()

    # Validate sizes
    if args.size_min < 0 or args.size_max <= 0 or args.size_min >= args.size_max:
        raise SystemExit("--size-min must be >=0 and < --size-max; --size-max must be >0")
    if args.grid_spacing <= 0:
        raise SystemExit("--grid-spacing must be > 0")
    if args.spiral_scale <= 0:
        raise SystemExit("--spiral-scale must be > 0")

    # Resolve size/preset
    if args.w and args.h:
        W, H = args.w, args.h
        preset = "custom"
    else:
        preset = (args.preset or "portrait1080").lower()
        W, H = PRESETS.get(preset, PRESETS["portrait1080"])

    # Batch vs single
    if args.batch and args.batch > 0:
        generate_batch(args, W, H, preset)
    else:
        if args.auto_seed or args.seed is None:
            seed_val = random.randrange(1, 10**9)
        else:
            seed_val = args.seed
        print("[1/1] Generating single output …")
        generate_one(seed_val, W, H, args, preset, idx=None, digits=2)

if __name__ == "__main__":
    main()
