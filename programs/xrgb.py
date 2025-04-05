from utils.ffmpeg_operations import run_ffmpeg_command

def xrgb(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]rgbashift=rh=185:rv=160:gh=-1:gv=6:bh=-6:bv=6:ah=-6:av=179,rgbashift=rh=2:rv=27:gh=48:gv=102:bh=3:bv=3:ah=-3:av=2,rgbashift=rh=6:rv=-6:gh=6:gv=-148:bh=16:bv=33:ah=-33:av=-9,rgbashift=rh=10:rv=202:gh=-151,rgbashift=rh=-31:rv=-30:gh=30:gv=-41:bh=78[out_v]",
        "-map", "[out_v]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-profile:v", "main",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with xrgb and file is {output_file}")
