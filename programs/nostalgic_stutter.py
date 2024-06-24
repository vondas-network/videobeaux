from utils.ffmpeg_operations import run_ffmpeg_command

def nostalgic_stutter(input_file, output_file):
    command = [
        "ffmpeg",
        "-y",
        "-i", input_file,
        "-filter_complex", "[0:v]random=frames=2:seed=212[1];[0:v]tmix=frames=3:weights=1 2 1 -3[4];[1]chromashift=cbh=192:cbv=-97:crh=-76:crv=81:edge=wrap,random=frames=2:seed=243[3];[4][3][0:v]mix=inputs=3:weights=2 1 1 [out_v]", 
        "-map", "[out_v]",
        "-map", "0:a",
        output_file
    ]

    run_ffmpeg_command(command)
    print(f"Video processed with nostalgic_stutter and file is {output_file}")