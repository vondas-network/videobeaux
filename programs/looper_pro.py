from utils.ffmpeg_operations import run_ffmpeg_command

def looper_pro(input_file, loop_count, size_in_frames, start_frame, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", f"[0:v]loop=loop={loop_count}:size={size_in_frames}:start={start_frame}[out_v]",
        "-map", "[out_v]",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with looper_pro and file is {output_file}")