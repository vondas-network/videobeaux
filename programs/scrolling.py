from utils.ffmpeg_operations import run_ffmpeg_command

def scrolling_video(input_file, output_file):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-filter_complex", f"[0:v]scroll=horizontal=0.0015:h=0.00:vertical=0.005[out_v]", 
        "-map", "[out_v]",
        "-map", "0:a",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with scrolling and file is {output_file}")