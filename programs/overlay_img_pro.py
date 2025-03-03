from utils.ffmpeg_operations import run_ffmpeg_command

def overlay_img_pro(input_file, output_file, overlay_image, x_position, y_position, overlay_height, overlay_width):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-i", overlay_image,
        "-filter_complex",  f"[1:v]scale={overlay_width}:{overlay_height}[ovr];[0:v][ovr]overlay={x_position}:{y_position}",
        "-map", "0:a",
        output_file 
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with overaly_img_pro and file is {output_file}")
