from utils.ffmpeg_operations import run_ffmpeg_command

def speed(input_file, speed_factor, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", f"[0:v]setpts=PTS/{speed_factor}[v];[0:a]atempo={speed_factor}[a]",
        "-map", "[v]",
        "-map", "[a]",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Changed the speed of the video and the file is {output_file}")
