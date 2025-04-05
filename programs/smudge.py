from utils.ffmpeg_operations import run_ffmpeg_command

def smudge(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]setrange=range=limited,tmedian=radius=7[out_v]",
        "-map", "[out_v]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-profile:v", "main",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with smudge and file is {output_file}")