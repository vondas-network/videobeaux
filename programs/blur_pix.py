from utils.ffmpeg_operations import run_ffmpeg_command

def blur_pix_video(input_file, output_file):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-filter_complex", "[0:v]pixelize=width=1:w=9:height=1:h=1,lagfun=decay=0.97:planes=1,tmix=frames=19,chromashift=cbh=-152:cbv=95:crh=-79:crv=142:edge=wrap[out_v]", 
        "-map", "[out_v]",
        "-map", "0:a",
        output_file
    ]
    run_ffmpeg_command(command)
    print(f"Video processed with blur_pix and file is {output_file}")
