from utils.ffmpeg_operations import run_ffmpeg_command

def steel_wash(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]shear,vibrance=intensity=0.36:rbal=2.44:gbal=1.13:bbal=-1.28:rlum=0.69:glum=0.35:blum=0.39[out_v]",
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
    print(f"Video processed with steel_wash and file is {output_file}")