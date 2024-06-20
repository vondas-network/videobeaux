from utils.ffmpeg_operations import run_ffmpeg_command

def frame_lag_video(input_file, num_of_frames, frame_weights, output_file):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-vf", f"tmix=frames={num_of_frames}:weights='{frame_weights}'",
        "-c:v", "libx264",
        "-crf", "23",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ac", "2",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with LSD and the file is {output_file} from {input_file}")

