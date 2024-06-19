from utils.ffmpeg_operations import run_ffmpeg_command

def extract_frames(input_file, output_folder, frame_rate):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-vf", f"fps={frame_rate}",
        f"{output_folder}/frame_%04d.png"
    ]
    run_ffmpeg_command(command)
    print(f"Frames extracted from {input_file} at {frame_rate} fps and saved to {output_folder}")
