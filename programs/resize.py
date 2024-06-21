from utils.ffmpeg_operations import run_ffmpeg_command

def resize(input_file, output_file, width, height):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-vf", f"scale={width}:{height}",
        output_file
    ]
    
    run_ffmpeg_command(command)
    print(f"Video resized to {width}x{height} and saved as {output_file}")
