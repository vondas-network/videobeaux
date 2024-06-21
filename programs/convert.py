from utils.ffmpeg_operations import run_ffmpeg_command

def convert(input_file, output_file, format):
    command = [
        "ffmpeg",
        "-i", input_file,
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video converted to {format} format and saved as {output_file}")
