from utils.ffmpeg_operations import run_ffmpeg_command

def digital_boss(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]huesaturation=hue=-131.18:saturation=0.56:intensity=0.18:strength=57.81:rw=0.75:gw=0.81,amplify=factor=10[out_v]",
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
    print(f"Video processed with digital_boss and file is {output_file}")

# ffmpeg -i shoe.mp4 -filter_complex "[0:v]shuffleplanes=map1=0:map3=2,smartblur=luma_radius=1.6:lr=2.88:luma_strength=0.11:lt=-17:cr=0.93,amplify=radius=33:factor=4:threshold=10721.12:tolerance=12[out_v]" -map "[out_v]" -map 0:a out.mp4
