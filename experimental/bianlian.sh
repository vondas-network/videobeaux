#! /bin/bash

# BASICS 
# python3 bianlian.py --preset portrait1080 --out mask.png --mode mask --auto-seed
# sleep 2
# python3 bianlian.py --preset 1080hd --out fixed.png --seed 12345
# sleep 2
# python3 bianlian.py --w 2048 --h 2048 --out square.png --auto-seed
# sleep 2

# Axis / Diagonal Mirrors

# python3 bianlian.py --preset widescreen --out hmirror.png --mirror horizontal --auto-seed
# sleep 2
# python3 bianlian.py --preset widescreen --out vmirror.png --mirror vertical --auto-seed
# sleep 2
# python3 bianlian.py --preset widescreen --out cross.png --mirror both --auto-seed
# sleep 2
# python3 bianlian.py --w 1920 --h 1080 --out diag.png --diag-mirror diag --auto-seed
# sleep 2
# python3 bianlian.py --w 1920 --h 1080 --out diagboth.png --diag-mirror both --auto-seed
# sleep 2
# python3 bianlian.py --preset 1080hd --out crossdiag.png --mirror both --diag-mirror both --auto-seed
# sleep 2

# Radial & Dihedral (Kaleidoscope)
# python3 bianlian.py --preset portrait1080 --out radial6.png --radial-sym 6 --auto-seed
# sleep 2
# python3 bianlian.py --preset portrait1080 --out d8.png --dihedral 8 --auto-seed
# sleep 2
# python3 bianlian.py --preset portrait1080 --out d8_r5.png --dihedral 8 --radial-sym 5 --auto-seed
# sleep 2
# python3 bianlian.py --w 1600 --h 1600 --out mega_kaleido.png --mirror both --diag-mirror both --dihedral 10 --auto-seed


# Grid & Spiral Copies
# python3 bianlian.py --preset widescreen --out grid3x2.png --grid 3x2 --grid-spacing 0.45 --auto-seed
# sleep 2
# python3 bianlian.py --w 2000 --h 1200 --out grid5x5.png --grid 5x5 --grid-spacing 0.35 --noise perlin --noise-scale 0.002 --noise-strength 0.1 --auto-seed
# sleep 2
# python3 bianlian.py --preset 1080hd --out spiral7.png --spiral 7 --spiral-rot-deg 25 --spiral-scale 1.06 --auto-seed
# sleep 2
# python3 bianlian.py --preset portrait1080 --out combo.png --grid 4x3 --grid-spacing 0.4 --spiral 5 --spiral-rot-deg 18 --spiral-scale 1.05 --dihedral 6 --auto-seed

# Noise-Driven Placement
# python3 bianlian.py --w 1920 --h 1080 --out perlin.png --noise perlin --noise-scale 0.0015 --noise-strength 0.22 --auto-seed
# sleep 2
# python3 bianlian.py --preset widescreen --out value.png --noise value --noise-scale 0.003 --noise-strength 0.2 --auto-seed
# sleep 2
# python3 bianlian.py --preset portrait1080 --out noisy_sym.png --noise perlin --noise-scale 0.002 --noise-strength 0.18 --mirror horizontal --radial-sym 7 --auto-seed

# Size, Fit & Frame Safety
# python3 bianlian.py --preset portrait1080 --out airy.png --size-min 0.12 --size-max 0.35 --auto-seed
# sleep 2
# python3 bianlian.py --preset widescreen --out bold.png --size-max 0.85 --margin 0.9 --auto-seed
# sleep 2
# python3 bianlian.py --preset 1080hd --out overflow.png --no-fit --no-keep-in-frame --auto-seed

# Color Mode (Preview)
# python3 bianlian.py --preset widescreen --out color_preview.png --mode color --bg "#0e0e0e" --auto-seed
# sleep 2
# python3 bianlian.py --w 1600 --h 900 --out color_combo.png --mode color --bg "#101622" --dihedral 12 --grid 4x2 --grid-spacing 0.5 --auto-seed

# Batch, Seeds, Metadata & Config
# python3 bianlian.py --preset portrait1080 --out mask.png --batch 12 --auto-seed
# sleep 3
# python3 bianlian.py --preset widescreen --out series.png --batch 8 --seed 9001
# sleep 3
# python3 bianlian.py --preset portrait1080 --out mask.png --config mask.json --batch 5 --auto-seed
# sleep 3
# python3 bianlian.py --w 2048 --h 2048 --out kscope.png --dihedral 9 --mirror both --diag-mirror both --config kscope.json --batch 4 --auto-seed

# “Looks like this” Recipes
# python3 bianlian.py --w 1600 --h 1600 --out rosette.png --radial-sym 10 --size-min 0.18 --size-max 0.32 --auto-seed
# sleep 2
# python3 bianlian.py --preset portrait1080 --out quilt.png --dihedral 8 --grid 3x3 --grid-spacing 0.38 --noise value --noise-strength 0.12 --auto-seed
# sleep 2
# python3 bianlian.py --preset 1080hd --out spinstar.png --spiral 9 --spiral-rot-deg 22 --spiral-scale 1.05 --mirror horizontal --auto-seed
# sleep 2
# python3 bianlian.py --w 3840 --h 2160 --out matte.png --mirror horizontal --size-min 0.08 --size-max 0.22 --auto-seed
# sleep 2
# python3 bianlian.py --preset portrait1080 --out quilt.png --dihedral 8 --grid 3x3 --grid-spacing 0.70 --size-min 0.10 --size-max 0.22 --planes 1 --auto-seed
# sleep 2
# python3 bianlian.py --preset portrait1080 --out quilt_preview.png --mode color --bg "#101622" --dihedral 8 --grid 3x3 --grid-spacing 0.60 --size-min 0.12 --size-max 0.28 --planes 2 --auto-seed


# Troubleshooting knobs
# python3 bianlian.py --preset portrait1080 --out lighter.png --size-min 0.1 --size-max 0.3 --margin 0.92 --auto-seed
# sleep 2
# python3 bianlian.py --preset 1080hd --out noisypos.png --noise perlin --noise-scale 0.002 --noise-strength 0.25 --size-min 0.2 --size-max 0.3 --auto-seed