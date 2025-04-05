from utils.ffmpeg_operations import run_ffmpeg_command

def wbflare(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]bilateral=sigmaS=377.67[out_v]",
        "-map", "[out_v]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-profile:v", "main",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with wbflare and file is {output_file}")