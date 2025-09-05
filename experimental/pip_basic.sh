#!/bin/bash
# PiP Overlay Examples Script
# Runs 10 PiP overlay commands with 2-second pauses between each

# python3 ./experimental/pip_basic.py -i ./media/example.mp4 -p ./media/menino.mp4 -o out_square.mp4 --pos tr --pip-percent 25 --feather 12 --border-width 6 --border-color "#FFFFFF"
# sleep 2

# python3 ./experimental/pip_basic.py -i ./media/example.mp4 -p ./media/menino.mp4 -o out_circle.mp4 --shape circle --pos c --pip-percent 40 --border-width 8 --border-color "0,255,255,0.7"
# sleep 2

# python3 ./experimental/pip_basic.py -i ./media/example.mp4 -p ./media/menino.mp4 -o out_triangle.mp4 --shape triangle --pos bl --pip-percent 30 --feather 18 --border-width 3 --border-color black
# sleep 2

# python3 ./experimental/pip_basic.py -i ./media/example.mp4 -p ./media/menino.mp4 -o out_rhombus.mp4 --shape rhombus --pos tl --pip-percent 20 --border-width 0
# sleep 2

# python3 ./experimental/pip_basic.py -i ./media/example.mp4 -p ./media/menino.mp4 -o out_masked.mp4 --shape mask --mask ./media/mask4.png --pos br --pip-percent 35 --border-width 10 --border-color "#FF00FFCC"
# sleep 2

# python3 ./experimental/pip_basic.py -i ./media/example.mp4 -p ./media/menino.mp4 -o out_px.mp4 --pip-width 640 --pip-height 360 --pos tr --border-width 4
# sleep 2

# python3 ./experimental/pip_basic.py -i ./media/example.mp4 -p ./media/menino.mp4 -o out_opacity.mp4 --pip-percent 30 --pip-opacity 0.85
# sleep 2

# python3 ./experimental/pip_basic.py -i ./media/example.mp4 -p ./media/menino.mp4 -o out_bigborder.mp4 --shape circle --pos br --pip-percent 25 --border-width 20 --border-color "#00FF00"
# sleep 2

# python3 ./experimental/pip_basic.py -i ./media/example.mp4 -p ./media/menino.mp4 -o out_softblur.mp4 --shape square --pos c --pip-percent 30 --feather 25 --border-width 5 --border-color blue
# sleep 2

python3 ./experimental/pip_basic.py -i ./media/example.mp4 -p ./media/menino.mp4 -o out_mixaudio.mp4 --pos tl --feather 1 --pip-percent 40 --audio mix --border-width 130 --border-color red 
# sleep 2

#!/bin/bash
# Clean PiP examples (NO flip/mirror). Sleep 2 between runs.
BG="./media/example.mp4"
PIP="./media/menino.mp4"
MASK="./media/mask4.png"

python3 ./experimental/pip_basic.py -i "./media/example.mp4" -p "./media/menino.mp4" -o out_square.mp4 --pos tr --pip-percent 25 --feather 2 --border-width 6 --border-color "#FFFFFF"
sleep 2

# python3 ./experimental/pip_basic.py -i "./media/example.mp4" -p "./media/menino.mp4" -o out_circle.mp4 --shape circle --pos c --pip-percent 40 --border-width 8 --border-color "0,255,255,0.7"
# sleep 2

# python3 ./experimental/pip_basic.py -i "./media/example.mp4" -p "./media/menino.mp4" -o out_triangle.mp4 --shape triangle --pos bl --pip-percent 30 --feather 18 --border-width 3 --border-color black
# sleep 2

# python3 ./experimental/pip_basic.py -i "./media/example.mp4" -p "./media/menino.mp4" -o out_rhombus.mp4 --shape rhombus --pos tl --pip-percent 20 --border-width 0
# sleep 2

# python3 ./experimental/pip_basic.py -i "./media/example.mp4" -p "./media/menino.mp4" -o out_masked.mp4 --shape mask --mask "./media/mask4.png" --pos br --pip-percent 35 --border-width 10 --border-color "#FF00FFCC"
# sleep 2

# python3 ./experimental/pip_basic.py -i "./media/example.mp4" -p "./media/menino.mp4" -o out_px.mp4 --pip-width 640 --pip-height 360 --pos tr --border-width 4
# sleep 2

python3 ./experimental/pip_basic.py -i "./media/example.mp4" -p "./media/menino.mp4" -o out_opacity.mp4 --pip-percent 30 --pip-opacity 0.85
# sleep 2

# python3 ./experimental/pip_basic.py -i "./media/example.mp4" -p "./media/menino.mp4" -o out_bigborder.mp4 --shape circle --pos br --pip-percent 25 --border-width 20 --border-color "#00FF00"
# sleep 2

# python3 ./experimental/pip_basic.py -i "./media/example.mp4" -p "./media/menino.mp4" -o out_softblur.mp4 --shape square --pos c --pip-percent 30 --feather 25 --border-width 5 --border-color blue
# sleep 2

# python3 ./experimental/pip_basic.py -i "./media/example.mp4" -p "./media/menino.mp4" -o out_mixaudio.mp4 --pos tl --pip-percent 20 --audio mix --border-width 6 --border-color red
# sleep 2

# # Extra rotation-only (safe) variants
python3 ./experimental/pip_basic.py -i "./media/example.mp4" -p "./media/menino.mp4" -o out_rotate15_circle.mp4 --shape circle --pos tr --pip-percent 32 --rotate 15 --border-width 10 --border-color "#00FFFF" --feather 10
sleep 2

# python3 ./experimental/pip_basic.py -i "./media/example.mp4" -p "./media/menino.mp4" -o out_rotate-10_rhombus.mp4 --shape rhombus --pos bl --pip-percent 28 --rotate -10 --border-width 6 --border-color black --feather 20
# sleep 2

# python3 ./experimental/pip_basic.py -i "./media/example.mp4" -p "./media/menino.mp4" -o out_rotate30_square.mp4 --shape square --pos tl --pip-percent 26 --rotate 30 --border-width 10 --border-color "#FF00FFCC" --feather 18
# sleep 2
