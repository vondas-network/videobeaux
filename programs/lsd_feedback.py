from utils.ffmpeg_operations import run_ffmpeg_command

def lsd_feedback(input_file, output_file):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-vf", "tmix=frames=8:weights=1 1 -3 2 1 1 -3 1",
        "-c:v", "libx264",
        "-crf", "23",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ac", "2",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with LSD and the file is {output_file} from {input_file}")