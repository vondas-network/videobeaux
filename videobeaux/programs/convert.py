from videobeaux.utils.ffmpeg_operations import run_ffmpeg_with_progress
from pathlib import Path
import sys

def register_arguments(parser):
    parser.description = "Converts input video into a stylized animation format. Requires output format like mp4 or mov."
    parser.add_argument(
        "--output-format",
        required=True,
        type=str,
        help="Format to convert output into (e.g. mp4, wav, etc). Output argument can just be a filename with no extension."
    )

def run(args):
    output_path = Path(args.output)
    clean_output = output_path.with_suffix(f".{args.output_format}")
    if clean_output.exists() and not args.force:
        print(f"❌ {clean_output} already exists. Use --force to overwrite.")
        sys.exit(1)

    command = [
        "ffmpeg",
        "-i", args.input,
        clean_output
    ]

    run_ffmpeg_with_progress((command[:1] + ["-y"] + command[1:]) if args.force else command, args.input, clean_output)
