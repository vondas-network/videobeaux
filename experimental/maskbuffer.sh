#!/bin/bash
# Run 20 maskbuffer.py examples with pauses
# Assumes maskbuffer.py, ./media/menino.mp4, ./media/example.mp4, mask.png, ./media/mask7.png, and ./media/menino.mp4.mp4 are available

# 1
python3 maskbuffer.py -i ./media/menino.mp4 -b ./media/example.mp4 -o ex01.mp4 \
  --mode mask --pattern sine --speed-x 4 --speed-y 6 --mask-size 420
sleep 2

# 2
python3 maskbuffer.py -i ./media/menino.mp4 -b ./media/example.mp4 -m ./media/mask7.png -o ex02.mp4 \
  --mode mask --pattern circle --speed-x 5 --speed-y 5 --mask-size 380 \
  --delay-frames 8 --trail-blur 1.0
sleep 2

# 3
python3 maskbuffer.py -i ./media/menino.mp4 -b ./media/example.mp4 -m ./media/mask7.png -o ex03.mp4 \
  --mode mask --pattern ellipse --speed-x 6 --speed-y 6 --mask-size 420 \
  --mask-key-type chromakey --mask-key-color "#00FF00" \
  --mask-key-similarity 0.28 --mask-key-blend 0.10 --mask-key-mix 1.0
sleep 2

# 4
python3 maskbuffer.py -i ./media/menino.mp4 -b ./media/example.mp4 -m ./media/mask7.png -o ex04.mp4 \
  --mode mask --pattern figure8 --speed-x 4 --speed-y 4 --mask-size 360 \
  --mask-key-type colorkey --mask-key-color "#00FFFF" \
  --mask-key-similarity 0.22 --mask-key-blend 0.06 --mask-key-mix 0.8
sleep 2 

# 5
python3 maskbuffer.py -i ./media/menino.mp4 -b ./media/example.mp4 -m ./media/mask7.png -o ex05.mp4 \
  --mode mask --pattern rose3 --speed-x 8 --speed-y 8 --mask-size 300 \
  --spin-period 5 --spin-phase-deg 45
sleep 2

# 6
python3 maskbuffer.py -i ./media/menino.mp4 -b ./media/example.mp4 -m ./media/mask7.png -o ex06.mp4 \
  --mode mask --pattern pingpong --speed-x 3 --speed-y 5 --mask-size 280 \
  --decay 0.85 --delay-frames 10 --trail-blur 0.8
sleep 2

# 7
# python3 maskbuffer.py -i ./media/menino.mp4 -b ./media/example.mp4 -m ./media/mask7.png -o ex07.mp4 \
#   --mode mask --pattern lissajous --speed-x 4 --speed-y 7 --mask-size 420 \
#   --duration-mode freeze
# sleep 2

# 8
python3 maskbuffer.py -i ./media/menino.mp4 -b ./media/example.mp4 -m ./media/mask7.png -o ex08.mp4 \
  --mode mask --pattern wrap --speed-x 120 --speed-y 80 --mask-size 240 \
  --spin-period 12
sleep 2

# 9
python3 maskbuffer.py -i ./media/menino.mp4 -b ./media/example.mp4 -m ./media/mask7.png -o ex09.mp4 \
  --mode mask --pattern gravity --speed-x 0.7 --speed-y 0.6 --mask-size 360 \
  --delay-frames 4 --trail-blur 0.5
sleep 2

# 10
python3 maskbuffer.py -i ./media/menino.mp4 -b ./media/example.mp4 -m ./media/mask7.png -o ex10.mp4 \
  --mode mask --randomize --speed-x 5 --speed-y 7 --mask-size 420 \
  --res 1920x1080 --fps 60
sleep 2

# 11
python3 maskbuffer.py -i ./media/menino.mp4 -b ./media/example.mp4 -m ./media/mask7.png -o ex11.mp4 \
  --mode mask --pattern sine --speed-x 9999 --speed-y 9999 --mask-size 420 \
  --spin-period 4
sleep 2

# 12
python3 maskbuffer.py -i ./media/menino.mp4 -b ./media/example.mp4 -m ./media/mask7.png -o ex12_alpha.webm \
  --mode mask --pattern circle --speed-x 5 --speed-y 5 --mask-size 380 \
  --alpha-out --codec libvpx-vp9 --pixfmt yuva420p --crf 28 --preset good
sleep 2

# 13
python3 maskbuffer.py -i ./media/menino.mp4 -b ./media/example.mp4 -m ./media/mask7.png -o ex13_alpha.mov \
  --mode mask --pattern figure8 --speed-x 6 --speed-y 3 --mask-size 400 \
  --alpha-out --codec prores_ks --pixfmt yuva444p10le --crf 18 --preset veryfast
sleep 2

# 14
python3 maskbuffer.py -i ./media/menino.mp4.mp4 -b ./media/example.mp4 -o ex14.mp4 \
  --mode ./media/menino.mp4 --pattern sine --speed-x 4 --speed-y 6 --mask-size 320 \
  --delay-frames 6 --trail-blur 0.8
sleep 2

# 15
python3 maskbuffer.py -i ./media/menino.mp4.mp4 -b ./media/example.mp4 -o ex15.mp4 \
  --mode ./media/menino.mp4 --pattern circle --speed-x 5 --speed-y 5 --mask-size 300 \
  --spin-period 6 --spin-phase-deg 15
sleep 2

# 16
python3 maskbuffer.py -i ./media/menino.mp4.mp4 -b ./media/example.mp4 -o ex16.mp4 \
  --mode ./media/menino.mp4 --pattern wrap --speed-x 150 --speed-y 90 --mask-size 260 \
  --spin-period 2
sleep 2

# 17
python3 maskbuffer.py -i ./media/menino.mp4.mp4 -b ./media/example.mp4 -o ex17.mp4 \
  --mode ./media/menino.mp4 --pattern figure8 --speed-x 4 --speed-y 4 --mask-size 280 \
  --duration-mode freeze
sleep 2

# 18
python3 maskbuffer.py -i ./media/menino.mp4.mp4 -b ./media/example.mp4 -o ex18.mp4 \
  --mode ./media/menino.mp4 --pattern rose3 --speed-x 8 --speed-y 8 --mask-size 300 \
  --crf 16 --preset slow
sleep 2

# 19
python3 maskbuffer.py -i ./media/menino.mp4 -b ./media/example.mp4 -m ./media/mask7.png -o ex19.mp4 \
  --mode mask --pattern ellipse --speed-x 6 --speed-y 6 --mask-size 360 \
  --mask-key-type chromakey --mask-key-color "#00FF00" \
  --mask-key-similarity 0.22 --mask-key-blend 0.08 --mask-key-mix 0.5
sleep 2

# 20
python3 maskbuffer.py -i ./media/menino.mp4 -b ./media/example.mp4 -o ex20.mp4 \
  --mode mask --pattern lissajous --speed-x 5 --speed-y 9 --mask-size 420 \
  --decay 0.82 --delay-frames 12 --trail-blur 1.2
sleep 2

#merged audio
python3 maskbuffer.py -i ./media/menino.mp4 -b ./media/example.mp4 -m ./media/mask7.png -o out_mix.mp4 \
  --mode mask --pattern circle --audio-mode mix
sleep 2

# video 1 audio
python3 maskbuffer.py -i ./media/menino.mp4 -b ./media/example.mp4 -m ./media/mask7.png -o out_fg_audio.mp4 \
  --mode mask --pattern circle --audio-mode 1
sleep 2

# video 2 audio
python3 maskbuffer.py -i ./media/menino.mp4 -b ./media/example.mp4 -m ./media/mask7.png -o out_bg_audio.mp4 \
  --mode mask --pattern circle --audio-mode 2
sleep 2

# auto
python3 maskbuffer.py -i ./media/menino.mp4 -b ./media/example.mp4 -m ./media/mask7.png -o out_auto.mp4 \
  --mode mask --pattern circle


python3 maskbuffer.py \
  -i ./media/menino.mp4 \
  -b ./media/example.mp4 \
  -m ./media/mask6.png \
  -o output.mp4 \
  --mode mask \
  --motion off \
  --mask-fullframe \
  --mask-blur 10 \
  --fg-brightness 0.05 \
  --fg-saturation 0.9 \
  --alpha-mul 0.85 \
  --audio-mode 1 \
  --codec libx264 --crf 18 --preset veryfast --res 1920x1080 --fps 30
