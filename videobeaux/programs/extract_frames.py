from videobeaux.utils.ffmpeg_operations import run_ffmpeg_with_progress
import os
from pathlib import Path
import sys

def register_arguments(parser):
    parser.description = (
            "Extract individuals frames from a video file and saves them as PNGs. \n"
            "--output should be a dir path, in which the PNGs will be saved."
    )
    parser.add_argument(
        "-fps", "--frame_rate",
        required=True,
        type=str,
        help="The number of PNGs extracted per second of video"
    )

def run(args):
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
        "-vf", f"fps={args.frame_rate}",
        f"{clean_output}/frame_%04d.png"
    ]
    
    run_ffmpeg_with_progress((command[:1] + ["-y"] + command[1:]) if args.force else command, args.input, clean_output)

