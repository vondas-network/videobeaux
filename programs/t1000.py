from utils.ffmpeg_operations import run_ffmpeg_command

def t1000(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]setrange=range=limited,tmedian=radius=19:percentile=0.47,rgbashift=rh=-2:rv=2:gh=-3:gv=3:bh=-4:bv=-2:ah=-12:av=3,tmedian=radius=9:percentile=0.32[out_v]",
        "-map", "[out_v]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-profile:v", "main",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with t1000 and file is {output_file}")

# -map 0:a -c:v libx264 -profile:v main -pix_fmt yuv420p -c:a aac out.mp4