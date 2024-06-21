from utils.ffmpeg_operations import run_ffmpeg_command

def frame_delay_pro2(input_file, decay, planes, output_file):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-vf", f"format=gbrp,lagfun=decay={decay}:planes={planes}",
        output_file
    ]

    run_ffmpeg_command(command)
    print(f"Video processed with frame_delay_pro2 and file is {output_file}")