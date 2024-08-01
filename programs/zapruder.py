from utils.ffmpeg_operations import run_ffmpeg_command

def zapruder(input_file, output_file):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-filter_complex", "[0:v]amplify=radius=2:factor=13:threshold=61889.14:tolerance=0.2,colorbalance,colorcorrect=rl=0.61:rh=0.2:bh=0.16:analyze=minmax,dctdnoiz=sigma=498.03[out_v]",
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
    print(f"Video processed with zapruder and file is {output_file}")

# ffmpeg -i shoe.mp4 -filter_complex "[0:v]shuffleplanes=map1=0:map3=2,smartblur=luma_radius=1.6:lr=2.88:luma_strength=0.11:lt=-17:cr=0.93,amplify=radius=33:factor=4:threshold=10721.12:tolerance=12[out_v]" -map "[out_v]" -map 0:a out.mp4
