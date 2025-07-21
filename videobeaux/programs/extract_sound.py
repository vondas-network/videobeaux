from videobeaux.utils.ffmpeg_operations import run_ffmpeg_with_progress
from pathlib import Path
import sys

def register_arguments(parser):
    parser.description = (
        "Extracts the audio as a .wav file from the --input video file."
    )
    print("✅ This program mode does not require additional arguments")

def run(args):
    output_path = Path(args.output)
    clean_output = output_path.with_suffix(f".wav")
    if clean_output.exists() and not args.force:
        print(f"❌ {clean_output} already exists. Use --force to overwrite.")
        sys.exit(1)
    command = [
        "ffmpeg",
        "-i", args.input,
        "-vn", 
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "2",
        clean_output
    ]
    
    run_ffmpeg_with_progress((command[:1] + ["-y"] + command[1:]) if args.force else command, args.input, clean_output)
