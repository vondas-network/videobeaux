# Step 1: Make the GIF transparent (replace 0xFFFFFF with your GIF's background color if not white)
ffmpeg -i comp.gif -vf "colorkey=0xFFFFFF:0.1" compfixed.gif

# Step 2: Overlay the transparent GIF on the video at position (100,100)
ffmpeg -i example.mp4 -i compfixed.gif -stream_loop -1 -filter_complex "[0:v][1:v]overlay=x=100:y=100:shortest=1" -c:a copy output_video.mp4

# Optional: Overlay with scaling (e.g., GIF width of 200 pixels) and centered position
# ffmpeg -i input_video.mp4 -i comp.gif -stream_loop -1 -filter_complex "[1:v]scale=200:-1:flags=lanczos[ov];[0:v][ov]overlay=x=(main_w-overlay_w)/2:y=(main_h-overlay_h)/2:shortest=1" -c:a copy output_scaled_video.mp4