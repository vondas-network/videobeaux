from utils.ffmpeg_operations import run_ffmpeg_command

def bad_animation(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]detelecine=first_field=bottom:pattern=5:start_frame=4[out_v]",
        "-map", "[out_v]",
        "-map", "0:a",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with bad_contrast and file is {output_file}")