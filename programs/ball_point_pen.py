from utils.ffmpeg_operations import run_ffmpeg_command

def ball_point_pen(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]amplify=radius=6:factor=2,bwdif=mode=send_frame:parity=bff,colorbalance=gs=-0.34:bs=0.47:rm=-0.18:gm=-0.7:bm=0.5[out_v]",
        "-map", "[out_v]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-profile:v", "high",
        "-level:v", "4.2",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-c:a", "copy",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with ball_point_pen and file is {output_file}")

# ffmpeg -i shoe.mp4 -filter_complex "[0:v]shuffleplanes=map1=0:map3=2,smartblur=luma_radius=1.6:lr=2.88:luma_strength=0.11:lt=-17:cr=0.93,amplify=radius=33:factor=4:threshold=10721.12:tolerance=12[out_v]" -map "[out_v]" -map 0:a out.mp4
