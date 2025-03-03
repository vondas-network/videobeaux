from utils.ffmpeg_operations import run_ffmpeg_command
from utils.ffprobe_operations import run_ffprobe_command
import time


def num_edits(input_file, output_file, count):
    command = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        input_file
    ]

    # duration=run_ffprobe_command(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $input_file)

    duration=run_ffprobe_command(command)

    print(duration)

    decoded_string = duration.decode('utf-8')
    stripped_string = decoded_string.strip()
    segment_duration = float(stripped_string)
    print(segment_duration)

    for number in range(int(count)):
        start_time=float(number) * segment_duration

        output_file=f"outputs/output_{number}.mp4"
        
        command = [
            "ffmpeg",
            "-i", input_file,
            "-ss", str(start_time),
            "-t", str(segment_duration),
            "-c", "copy",
            output_file
        ]        

        print(command)
        run_ffmpeg_command(command)
        time.sleep(5)




    # # Split the video into even pieces
    # for ((i=0; i<count; i++))
    #     start_time=$(echo "$i * $segment_duration" | bc -l)
    #     do
    #         command = [
    #         "ffmpeg",
    #         "-i", input_file,
    #         "-ss", "format=duration",
    #         "-of", "default=noprint_wrappers=1:nokey=1",
    #         input_file
    #     ]

    #     output_file="$output_dir/output_$i.mp4"
    #     ffmpeg -i $input_video -ss $start_time -t $segment_duration -c copy $output_file

    #     run_ffmpeg_command(command)

    # done



    print(f"Video resized to  and saved as")




