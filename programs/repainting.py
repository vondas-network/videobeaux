from utils.ffmpeg_operations import run_ffmpeg_command

def repainting(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]median=radius=127:radiusV=15:percentile=0.93[3];[0:v]tmix=frames=20:weights=1 2 3 -2 1 2 3 -2 1 -4 4 2 3 -2 1 2 3 -2 1 1[7];[3][7]mix,lagfun=decay=1[out_v]",
        "-map", "[out_v]",
        "-map", "0:a",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with repainting and file is {output_file}")