from utils.ffmpeg_operations import run_ffmpeg_command

def scrolling_pro(input_file, output_file, horizontal, vertical):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-filter_complex", f"[0:v]scroll=horizontal={horizontal}:vertical={vertical}[out_v]", 
        "-map", "[out_v]",
        "-map", "0:a",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with scrolling_pro and file is {output_file}")