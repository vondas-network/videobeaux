from utils.ffmpeg_operations import run_ffmpeg_command

def recalled_sensor(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]shuffleplanes=map1=0:map3=2,smartblur=luma_radius=1.6:lr=2.88:luma_strength=0.11:lt=-17:cr=0.93,amplify=radius=14:factor=4139[out_v]",
        "-map", "[out_v]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-profile:v", "main",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with recalled_sensor and file is {output_file}")
