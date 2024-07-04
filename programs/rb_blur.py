from utils.ffmpeg_operations import run_ffmpeg_command

def rb_blur(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]gradfun=strength=64:radius=5[out_v]",
        "-map", "[out_v]",
        # "-map", "0:a",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with rb_blur and file is {output_file}")
