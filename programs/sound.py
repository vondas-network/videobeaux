from utils.ffmpeg_operations import run_ffmpeg_command

def extract_sound(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-vn", 
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "2",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Audio extracted from video using sound and file is {output_file}")