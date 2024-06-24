from utils.ffmpeg_operations import run_ffmpeg_command

def overexposed_stutter(input_file, output_file):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-filter_complex", "[0:v]tblend=c0_mode=or:c1_mode=freeze:c2_mode=negation:c3_mode=geometric:all_mode=vividlight,random=frames=2,lagfun[out_v]", 
        "-map", "[out_v]",
        "-map", "0:a",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with overexposed_stutter and file is {output_file}")