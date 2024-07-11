from utils.ffmpeg_operations import run_ffmpeg_command

def light_snow(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]minterpolate,chromashift=cbh=-5.7:cbv=22:crh=1.44:crv=10.8,deband=1thr=0.45003:2thr=0.48003:3thr=0.21003:4thr=0.30003:range=-1.3:r=16:d=1.69681[out_v]",
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
    print(f"Video processed with light_snow and file is {output_file}")
