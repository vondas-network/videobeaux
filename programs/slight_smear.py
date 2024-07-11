from utils.ffmpeg_operations import run_ffmpeg_command

def slight_smear(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]rgbashift=rh=3:rv=2:gh=1:gv=-3:bh=-1:bv=3:ah=-1:av=-1:edge=wrap[out_v]",
        "-map", "[out_v]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-profile:v", "high",
        "-level:v", "4.2",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-c:a", "aac",
        "-b:a", "128",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with slight_smear and file is {output_file}")
