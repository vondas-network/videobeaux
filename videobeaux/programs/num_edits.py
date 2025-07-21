from videobeaux.utils.ffmpeg_operations import run_ffmpeg_with_progress
from videobeaux.utils.ffprobe_operations import run_ffprobe_command
from pathlib import Path
import time
import sys
import os

"""
TODO: 
--------------------------------
- This currently does not work.

"""

def register_arguments(parser):
    parser.description = (
        "Splits the video up into the number of user defined sections."
        "--output is a directory where snippets will be stored as .mp4s"
    )
    parser.add_argument(
        "--count",
        required=True,
        type=str,
        help="Number of pieces to split the --input video into."
    )


def run(args):

    command = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        args.input
    ]

    # duration=run_ffprobe_command(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $input_file)

    duration=run_ffprobe_command(command)

    print(duration)

    decoded_string = duration.decode('utf-8')
    stripped_string = decoded_string.strip()
    segment_duration = float(stripped_string)
    print(segment_duration)

    for number in range(int(args.count)):
        start_time=float(number) * segment_duration
        output_path = Path(args.output)
        clean_output = output_path.with_suffix("")
        print(clean_output)
        if clean_output.exists() and not args.force:
            print(f"❌ {clean_output} already exists. Use --force to overwrite.")
            sys.exit(1)
        if not os.path.exists(clean_output):
            os.makedirs(clean_output)        
        command = [
            "ffmpeg",
            "-i", args.input,
            "-ss", str(start_time),
            "-t", str(segment_duration),
            "-c", "copy",
            f"{args.output}_{number}"
        ]        

        print(command)
        run_ffmpeg_with_progress((command[:1] + ["-y"] + command[1:]) if args.force else command, args.input, args.output)

        time.sleep(5)




