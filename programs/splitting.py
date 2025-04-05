from utils.ffmpeg_operations import run_ffmpeg_command

def splitting(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]shuffleplanes,shufflepixels=direction=inverse:m=vertical:width=157[2];[0:v][2]mix[out_v]",
        "-map", "[out_v]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-profile:v", "main",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with splitting and file is {output_file}")
