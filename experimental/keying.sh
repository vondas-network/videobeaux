
## COLORKEY
## 0x00FF00 = key color, 0.25 = similarity, 0.08 = blend/soften.
ffmpeg -i ./media/meninochain4.mp4 -i ./media/meninomask.mp4 -filter_complex "[0:v]colorkey=0x00FF00:0.25:0.38[cut];[1:v][cut]overlay=0:0[out]" -map "[out]" -map 0:a -c:v libx264 -crf 18 -preset veryfast -c:a aac out_colorkey.mp4
ffmpeg -i ./media/meninochain2.mp4  -i ./media/meninochain4.mp4 -filter_complex "[0:v]colorkey=0x00AA00:0.25:0.08[cut];[1:v][cut]overlay=0:0[out]" -map "[out]" -map 0:a -c:v libx264 -crf 18 -preset veryfast -c:a aac out_colorkey.mp4

## CHROMAKEY
## Add :yuv=1 if you want the hex color interpreted as YUV. Edge handling differs from colorkey
ffmpeg -i ./media/meninochain4.mp4 -i ./media/meninochain.mp4 -filter_complex "[0:v]chromakey=f3f6f4:0.25:0.18[cut];[1:v][cut]overlay[out]" -map "[out]" -map 0:a -c:v libx264 -crf 18 -preset veryfast -c:a aac out_chromakey.mp4


## LUMA 
## threshold (0–1), tolerance, softness control the matte
ffmpeg -i ./media/meninochain.mp4  -i ./media/meninochain4.mp4 -filter_complex "[0:v]lumakey=0.15:0.05:0.02[cut];[1:v][cut]overlay[out]" -map "[out]" -map 0:a -c:v libx264 -crf 18 -preset veryfast -c:a aac out_lumakey.mp4

## ALPHAMERGE
# Inputs: 0=foreground color; 1=grayscale matte (white=keep, black=transparent); 2=background
# Pair with alphaextract if you first need to peel alpha out of an RGBA source.
ffmpeg -i ./media/meninochain.mp4  -i ./media/menino.mp4 -i ./media/meninomask.mp4 -filter_complex "[1:v]format=gray[m];[0:v][m]alphamerge[fg_a];[2:v][fg_a]overlay[out]" -map "[out]" -map 0:a -c:v libx264 -crf 18 -preset veryfast -c:a aac out_alphamerge.mp4

## Hard-mask compositing (PNG mask)
# Same mechanics as #4, but with a still mask image. CHECK
ffmpeg -i ./media/meninochain.mp4  -i ./media/mask2.png -i ./media/meninomask.mp4  -filter_complex "[1:v]format=gray[m];[0:v][m]alphamerge[fg_a];[2:v][fg_a]overlay[out]" -map "[out]" -c:v libx264 -crf 18 -preset veryfast out_mask.png.mp4

## Difference key with a clean plate (background subtraction) CHECK
# blend=...difference gives a motion/plate difference, blurred then hard-thresholded into a matte.
# Inputs: 0=scene with subject; 1=clean-plate image; 2=new background
ffmpeg -i ./media/meninochain.mp4  -i ./media/mask2.png -i ./media/meninomask.mp4 -filter_complex "[0:v][1:v]blend=all_mode=difference,format=gray,boxblur=5:1,lut=if(gt(val\,40)\,255\,0)[m]; [0:v][m]alphamerge[fg_a]; [2:v][fg_a]overlay[out]" -map "[out]" -c:v libx264 -crf 18 -preset veryfast out_diffkey.mp4

## Motion/difference key (no clean plate): tblend (temporal difference)
# Great for “reveal moving parts only” looks; tune the threshold and blur.
# Inputs: 0=single moving-subject clip; 1=new background
ffmpeg -i ./media/meninomask.mp4  -i ./media/meninochain4.mp4 -filter_complex "[0:v]tblend=all_mode=difference,format=gray,boxblur=5:1,lut=if(gt(val\,30)\,255\,0)[m]; [0:v][m]alphamerge[fg_a]; [1:v][fg_a]overlay[out]" -map "[out]" -c:v libx264 -crf 18 -preset veryfast out_motionkey.mp4



## Soft feedback trail with lagfun (simple & nice)
# decay ~0.90–0.98 controls how long the trail lingers.
ffmpeg -i ./media/meninochain.mp4  -i ./media/meninochain.mp4 \
-filter_complex "
  [0:v]colorkey=a0fffc:0.45:0.08,format=rgba[k];
  [k]lagfun=decay=0.96[trail];
  [1:v][trail]overlay=0:0[out]
" \
-map "[out]" -map 0:a -c:v libx264 -crf 18 -preset veryfast -c:a aac out_colorkey_lagfun.mp4
