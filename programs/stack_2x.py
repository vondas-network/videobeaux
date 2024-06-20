from utils.ffmpeg_operations import run_ffmpeg_command

def stack_2x_video(input_file1, input_file2, output_file):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file1,
        "-i", input_file2,
        "-filter_complex", "[0:v][1:v]vstack=inputs=2[v]; [0:a][1:a]amerge=inputs=2[a]", 
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-crf", "23",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ac", "2",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video reversed and saved as {output_file} from {input_file1} and {input_file2}")

