from utils.ffmpeg_operations import run_ffmpeg_command

def bad_contrast(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]unsharp=luma_msize_x=9:lx=11:luma_amount=-0.26,tblend=c0_mode=reflect:c1_mode=hardmix:c2_mode=vividlight:c3_mode=exclusion:all_mode=grainmerge[out_v]",
        "-map", "[out_v]",
        "-map", "0:a",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with bad_contrast and file is {output_file}")