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





ffmpeg -i "$MAIN_VIDEO" -i "$PIP_VIDEO" \
-filter_complex "[1:v]scale=${PIP_WIDTH}:${PIP_HEIGHT}[pip]; \
                [0:v][pip]overlay=x='if(gte(mod(t,10),5), ${BOUNCE_X_END} + (mod(t,5)) * (${BOUNCE_X_START} - ${BOUNCE_X_END}) / 5, ${BOUNCE_X_START} - (mod(t,5)) * (${BOUNCE_X_START} - ${BOUNCE_X_END}) / 5)':y='if(gte(mod(t,10),5), ${BOUNCE_Y_END} + (mod(t,5)) * (${BOUNCE_Y_START} - ${BOUNCE_Y_END}) / 5, ${BOUNCE_Y_START} - (mod(t,5)) * (${BOUNCE_Y_START} - ${BOUNCE_Y_END}) / 5)'[v]; \
                [0:a][1:a]amix=inputs=2[a]" \
-map "[v]" -map "[a]" \
-t $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$MAIN_VIDEO") \
-c:v libx264 -preset veryfast -crf 23 \
-c:a aac -b:a 192k \
"$OUTPUT_FILE"