from utils.ffmpeg_operations import run_ffmpeg_command

def twociz(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]amplify=radius=8:factor=14624.74,chromakey=color=blue:similarity=0.11001:blend=0.24[out_v]",
        "-map", "[out_v]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-profile:v", "main",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with twociz and file is {output_file}")
