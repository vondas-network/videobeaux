from utils.ffmpeg_operations import run_ffmpeg_command

def soapblind(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]owdenoise=depth=11:luma_strength=330.06:ls=450.02:chroma_strength=440.1:cs=220.21[out_v]",
        "-map", "[out_v]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-profile:v", "main",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with soapblind and file is {output_file}")
