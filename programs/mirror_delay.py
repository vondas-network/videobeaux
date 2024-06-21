from utils.ffmpeg_operations import run_ffmpeg_command

def mirror_delay(input_file, output_file):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-filter_complex", "[0:v]copy[1];[0:v]tmix=frames=8:weights=1 1 -3 2 1 1 -3 1[3];[1]hflip[2];[0:v][2][3]mix=inputs=3[out_v]", 
        "-map", "[out_v]",
        "-map", "0:a",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with mirror_delay and file is {output_file}")