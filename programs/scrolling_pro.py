from utils.ffmpeg_operations import run_ffmpeg_command

def scrolling_pro_video(input_file, horizontal, vertical, output_file):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-filter_complex", f"[0:v]scroll=horizontal={horizontal}:h=0.00:vertical={vertical}[out_v]", 
        "-map", "[out_v]",
        "-map", "0:a",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with scrolling_pro and file is {output_file}")
