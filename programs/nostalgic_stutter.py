from utils.ffmpeg_operations import run_ffmpeg_command

def nostalgic_stutter_video(input_file, output_file):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-filter_complex", "[0:v]random=frames=4:seed=312[1];[0:v]tmix=frames=7:weights=3 -2 4 1 1 1 -3[4];[1]chromashift=cbh=112:cbv=-97:crh=-76:crv=81:edge=wrap,random=frames=8:seed=3[3];[4][3][0:v]mix=inputs=3:weights=1 1 1 [out_v]", 
        "-map", "[out_v]",
        "-map", "0:a",
        output_file
    ]

    run_ffmpeg_command(command)
    print(f"Video processed with nostalgic_stutter and file is {output_file}")