from utils.ffmpeg_operations import run_ffmpeg_command

def stutter_pro_video(input_file, stutter, output_file):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-filter_complex", f"[0:v]random=frames={stutter}[out_v]", 
        "-map", "[out_v]",
        "-map", "0:a",
        output_file
    ]

    run_ffmpeg_command(command)
    print(f"Video processed with stutter_pro and file is {output_file}")
