from utils.ffmpeg_operations import run_ffmpeg_command

def septic(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]vibrance=intensity=0.74:rbal=0:gbal=4.72:rlum=0.3:glum=0.26:blum=0.72[out_v]",
        "-map", "[out_v]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-profile:v", "main",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with septic and file is {output_file}")
