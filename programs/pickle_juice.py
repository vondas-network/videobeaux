from utils.ffmpeg_operations import run_ffmpeg_command

def pickle_juice(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]shear,vibrance=intensity=0.36:rbal=2.94:gbal=3.34:bbal=-3.83:rlum=0.41:glum=0.15:blum=0.28[out_v]",
        "-map", "[out_v]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-profile:v", "high",
        "-level:v", "4.2",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-c:a", "copy",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with pickle_juice and file is {output_file}")