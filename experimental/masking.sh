ffmpeg \
  -i jitter_output.mp4 \
  -i hard_cut.mp4 \
  -i mask2.png \
  -filter_complex "[1:v][2:v]alphamerge[fg];[0:v][fg]overlay[out]" \
  -map "[out]" -c:v libx264 -crf 18 -preset veryfast output.mp4


ffmpeg \
  -i meninomask.mp4 \
  -i meninomask3.mp4 \
  -i mask2.png \
  -filter_complex "
    [0:v]scale=1920:1080[bg];                                        \
    [1:v]scale=1920:1080[fgraw];                                     \
    [2:v]scale=1920:1080,format=gray,boxblur=10:1[mask];             \
    [fgraw][mask]alphamerge[fg];                                     \
    [bg][fg]overlay[out]
  " \
  -map "[out]"  -c:v libx264 -crf 18 -preset veryfast  output.mp4


ffmpeg \
  -i menino.mp4 \
  -i zoom_blur_output.mp4 \
  -i mask4.png \
  -filter_complex "
    [0:v]scale=1920:1080[bg];                                       \
    [1:v]scale=1920:1080,eq=brightness=0.05:saturation=0.9[fgraw];  \
    [2:v]scale=1920:1080,format=gray,boxblur=10:1[mask];            \
    [fgraw][mask]alphamerge[fg];                                    \
    [fg]format=rgba,colorchannelmixer=aa=0.85[fgsoft];              \
    [bg][fgsoft]overlay[out]
  " \
  -map "[out]" -map 0:a -c:v libx264 -crf 18 -preset veryfast output.mp4

ffmpeg \
  -i crows1.mp4 \
  -i crows2.mp4 \
  -i mask2.png \
  -filter_complex "
    [0:v]scale=1920:1080[bg];                                       \
    [1:v]scale=1920:1080,eq=brightness=0.05:saturation=0.9[fgraw];  \
    [2:v]scale=1920:1080,format=gray,boxblur=10:1[mask];            \
    [fgraw][mask]alphamerge[fg];                                    \
    [fg]format=rgba,colorchannelmixer=aa=0.85[fgsoft];              \
    [bg][fgsoft]overlay[out]
  " \
  -map "[out]" -map 0:a -c:v libx264 -c:a aac -crf 18 -preset veryfast outpu3t.mp4

  ffmpeg \
  -i crows1.mp4 \
  -i crows2.mp4 \
  -i mask2.png \
  -filter_complex "
    [0:v]scale=1920:1080[bg];                                       \
    [1:v]scale=1920:1080,eq=brightness=0.05:saturation=0.89[fgraw];  \
    [2:v]scale=1920:1080,format=gray,boxblur=7:1[mask];            \
    [fgraw][mask]alphamerge[fg];                                    \
    [fg]format=rgba,colorchannelmixer=aa=0.45[fgsoft];              \
    [bg][fgsoft]blend=all_mode=overlay[out]
  " \
  -map "[out]" -map 0:a -c:v libx264 -c:a aac -crf 18 -preset veryfast out22put.mp4

    ffmpeg \
  -i meninoburst.mp4 \
  -i menino.mp4 \
  -i mask4.png \
  -filter_complex "
    [0:v]scale=1920:1080[bg];                                       \
    [1:v]scale=1920:1080,eq=brightness=0.55:saturation=0.89[fgraw];  \
    [2:v]scale=1920:1080,format=gray,boxblur=7:1[mask];            \
    [fgraw][mask]alphamerge[fg];                                    \
    [fg]format=rgba,colorchannelmixer=aa=0.25[fgsoft];              \
    [bg][fgsoft]blend=all_mode=overlay[out]
  " \
  -map "[out]" -map 0:a -c:v libx264 -c:a aac -crf 18 -preset veryfast out22put.mp4


### BLENDING AND OVERLAYING
ffmpeg -i ./media/example.mp4 -i ./media/example_bp.mp4 -i ./media/mask5.png -filter_complex "[0:v][2:v]overlay[out]" output_blendmask.mp4

### ?
ffmpeg -i ./media/example.mp4 -i ./media/example_bp.mp4 -i ./media/mask4.png -filter_complex "
[2:v]format=gray,scale=640x480[mask];
[0:v]scale=640x480,format=rgba[main];
[1:v]scale=640x480,format=rgba,lagfun=decay=0.99,edgedetect=low=0.1:high=0.3[bgfx];
[bgfx][mask]alphamerge[masked_bg];
[main][masked_bg]overlay=format=auto:x='5*sin(t*5)':y='5*cos(t*3)'[weird];
[weird]split=2[base][glitch];
[glitch]curves=r='0/0 0.3/0.5 1/1':g='0/0 0.6/0.4 1/1':b='0/0 0.1/0.9 1/1',boxblur=2:1[glitched];
[base][glitched]blend=all_mode=screen,format=yuv420p[out]
" -map "[out]" -c:v libx264 -crf 18 -preset slow output1_fixed.mp4

###
ffmpeg -i ./media/example.mp4 -i ./media/example_bp.mp4  -i ./media/mask4.png -filter_complex "
[2:v]format=gray,scale=640x480[mask];
[1:v]scale=640x480,format=rgba,
   lutrgb='r=val*0.8:g=val*0.6:b=val*1.2',
   hue=s=0,
   noise=alls=20:allf=t+u,
   curves=preset=negative[corrupt];
[0:v]scale=640x480,format=rgba[main];
[corrupt][mask]alphamerge[masked_corrupt];
[main][masked_corrupt]overlay=format=auto,format=yuv420p[out]
" -map "[out]" -c:v libx264 -preset veryslow -crf 20 output2_fixed.mp4


ffmpeg -i ./media/example.mp4 -i ./media/example_bp.mp4 -i ./media/mask4.png -filter_complex "
[2:v]format=gray,scale=640x360[mask];
[0:v]scale=640x360,boxblur=2:1,zoompan=z='1.01':x='iw/2-(iw/2)*1.01':y='ih/2-(ih/2)*1.01':d=1,format=rgba[spiral];
[1:v]scale=640x360,edgedetect=low=0.3:high=0.6,format=rgba[bg];
[spiral][mask]alphamerge[masked_spiral];
[bg][masked_spiral]overlay=format=auto,format=yuv420p[out]
" -map "[out]" -c:v libx264 -crf 18 -preset medium output3_fixed.mp4


### BLACK AND WHITE CRT
ffmpeg -i ./media/example.mp4 -filter_complex "\
[0:v]scale=640x480,format=yuv420p[base]; \
[base]eq=contrast=1.2:brightness=0.05:saturation=1.4,boxblur=2:1,tblend=all_mode=lighten[glow]; \
[base][glow]blend=all_mode=overlay[crt_core]; \
[crt_core]split=2[vid][scan]; \
[scan]geq='lum(X,Y)*(mod(Y\,2))':cb=128:cr=128[scanline]; \
[vid][scanline]overlay[out]" \
-map "[out]" -c:v libx264 -crf 18 -preset slow output_crt_glow.mp4

ffmpeg -i ./media/example.mp4 -filter_complex "\
[0:v]scale=640x480,format=rgba[base]; \
[base]eq=contrast=1.2:brightness=0.05:saturation=1.4,boxblur=2:1,tblend=all_mode=lighten[glow]; \
[base][glow]blend=all_mode=overlay[crt_core]; \
[crt_core]split=2[vid][scan]; \
[scan]geq='lum(X,Y)':a='255*mod(Y\,2)'[scanline]; \
[vid][scanline]overlay[post]; \
[post]format=yuv420p[out]" \
-map "[out]" -c:v libx264 -crf 18 -preset slow output_crt_color.mp4

### COLOR CRT
ffmpeg -i ./media/example.mp4 -filter_complex "\
[0:v]scale=640x480,format=rgba[base]; \
[base]eq=contrast=1.2:brightness=0.05:saturation=1.4,boxblur=2:1,tblend=all_mode=lighten[glow]; \
[base][glow]blend=all_mode=overlay[crt_core]; \
nullsrc=size=640x480:duration=10:rate=30,format=rgba[scanlines]; \
[scanlines]drawbox=x=0:y=0:w=640:h=1:color=black@0.2:t=fill, \
           drawbox=x=0:y=2:w=640:h=1:color=black@0.2:t=fill, \
           drawbox=x=0:y=4:w=640:h=1:color=black@0.2:t=fill, \
           drawbox=x=0:y=6:w=640:h=1:color=black@0.2:t=fill[pattern]; \
[crt_core][pattern]overlay[post]; \
[post]format=yuv420p[out]" \
-map "[out]" -c:v libx264 -crf 18 -preset slow output_crt_scanlines_fixed.mp4

### POSTERIZE
ffmpeg -i ./media/example.mp4 -filter_complex "\
[0:v]format=yuv420p,curves=r='0/0 0.5/0.3 1/1':g='0/0 0.3/0.7 1/1':b='0/0 0.2/1 1/0.9',hue=s=2[fx]" \
-map "[fx]" -c:v libx264 -pix_fmt yuv420p -profile:v high -crf 18 -preset slow "test-posterize-$(date +%Y%m%d-%H%M%S).mp4"

### LUMA MASK BLEND
ffmpeg -i ./media/example.mp4 -filter_complex "\
[0:v]split=2[base][copy]; \
[copy]boxblur=2:1,hue=s=0,curves=preset=negative[processed]; \
[0:v]format=gray,lut='val*2'[mask_raw]; \
[mask_raw]scale=640x480[mask]; \
[processed][mask]alphamerge[masked]; \
[base][masked]overlay[fx]" \
-map "[fx]" -c:v libx264 -pix_fmt yuv420p -profile:v high -crf 18 -preset slow "test-lumamask-$(date +%Y%m%d-%H%M%S).mp4"


### FEEDBACK TRAILS
ffmpeg -i ./media/example.mp4 -filter_complex "\
[0:v]format=rgba,lagfun=decay=0.96,tblend=all_mode=lighten[fx]" \
-map "[fx]" -c:v libx264 -pix_fmt yuv420p -profile:v high -crf 20 -preset slow "test-feedback-$(date +%Y%m%d-%H%M%S).mp4"

ffmpeg -i ./media/example.mp4 -filter_complex "\
[0:v]format=rgba,lagfun=decay=0.99,tblend=all_mode=lighten[fx]" \
-map "[fx]" -c:v libx264 -pix_fmt yuv420p -profile:v high -crf 20 -preset slow "test-feedback-$(date +%Y%m%d-%H%M%S).mp4"


### pagecurlfx
ffmpeg -i ./media/example.mp4 -filter_complex "\
[0:v]format=rgba, \
curves=r='0/0 0.5/0.3 1/1':g='0/0 0.3/0.7 1/1':b='0/0 0.2/1 1/0.9', \
hue=s=2, \
lagfun=decay=0.96, \
tblend=all_mode=lighten, \
lenscorrection=k1=-0.25:k2=0.05, \
format=yuv420p[fx]" \
-map "[fx]" -c:v libx264 -pix_fmt yuv420p -profile:v high -crf 18 -preset slow "test-posterize-feedback-lenswarp-$(date +%Y%m%d-%H%M%S).mp4"



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
