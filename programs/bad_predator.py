from utils.ffmpeg_operations import run_ffmpeg_command

def bad_predator(input_file1, input_file2, output_file):
    command = [
        "ffmpeg",
        "-i", input_file1,
        "-filter_complex", "[0:v]shuffleplanes,smartblur=luma_radius=1.6:lr=2.88:luma_strength=0.11:lt=-17:cr=0.93,amplify=radius=33:factor=4:threshold=10721.12:tolerance=12:low=12420.26:high=49802.12,despill=mix=0.58:expand=0.85:red=-1.2:green=1.21:blue=2.3:brightness=4.45:alpha=true,lagfun=decay=0.85[out_v]",
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
    print(f"Video processed with bad_predator and file is {output_file}")

