from utils.ffmpeg_operations import run_ffmpeg_command

def broken_scroll(input_file, output_file):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-filter_complex", f"[0:v]amplify=radius=12:factor=12:low=17213.43:high=4310.24,scroll=h=0.003:v=1:vpos=.2[out_v]", 
        "-map", "[out_v]",
        "-map", "0:a",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with broken_scroll and file is {output_file}")
