from utils.ffmpeg_operations import run_ffmpeg_command

def reverse_video(input_file, output_file):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-vf", "reverse", 
        "-af", "areverse",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video reversed and saved as {output_file} from {input_file}")