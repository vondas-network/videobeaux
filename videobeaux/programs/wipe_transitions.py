from videobeaux.utils.ffmpeg_operations import run_ffmpeg_with_progress
from pathlib import Path
import sys
import subprocess

# List of supported xfade transition presets
VIDEO_TRANSITIONS = [
    "fade", "wipeleft", "wiperight", "wipeup", "wipedown",
    "slideleft", "slideright", "slideup", "slidedown",
    "circlecrop", "circleclose", "circleopen",
    "horizopen", "horizclose", "vertopen", "vertclose",
    "dissolve", "pixelize",
    "diagtl", "diagtr", "diagbl", "diagbr",
    "hlslice", "hrslice", "vuslice", "vdslice",
    "hblur", "fadeblack", "fadewhite",
    "radial", "smoothleft", "smoothright", "smoothup", "smoothdown",
    "rectcrop", "distance", "fadegrays",
    "squeezeh", "squeezev", "zoomin"
]

def get_video_duration(input_file):
    """Get the duration of a video file using ffprobe."""
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(input_file)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        print(f"❌ Error getting duration for {input_file}: {result.stderr}")
        sys.exit(1)
    try:
        return float(result.stdout.strip())
    except ValueError:
        print(f"❌ Invalid duration for {input_file}")
        sys.exit(1)

def register_arguments(parser):
    parser.description = "Combines two input videos with a transitional wipe using FFmpeg's xfade filter. Supports various preset transitions and customizable duration."
    parser.add_argument(
        "--input1",
        required=True,
        type=str,
        help="Path to the first input video."
    )
    parser.add_argument(
        "--input2",
        required=True,
        type=str,
        help="Path to the second input video."
    )
    parser.add_argument(
        "--output-format",
        required=True,
        type=str,
        help="Format to convert output into (e.g., mp4, mov, etc). Output argument can just be a filename with no extension."
    )
    parser.add_argument(
        "--preset",
        required=True,
        type=str,
        choices=VIDEO_TRANSITIONS,
        help="Preset transition type (e.g., wipeleft, fade, etc)."
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=1.0,
        help="Duration of the transition in seconds (default: 1.0). Can be long for artistic effects, but may be capped by clip lengths."
    )
    parser.add_argument(
        "--offset",
        type=float,
        default=None,
        help="Offset in seconds where the transition starts in the first video (default: end of first video minus duration)."
    )

def run(args):
    output_path = Path(args.output)
    clean_output = output_path.with_suffix(f".{args.output_format}")
    
    if clean_output.exists() and not args.force:
        print(f"❌ {clean_output} already exists. Use --force to overwrite.")
        sys.exit(1)

    # Get durations
    dur1 = get_video_duration(args.input1)
    dur2 = get_video_duration(args.input2)
    
    # Set offset if not provided
    if args.offset is None:
        args.offset = max(0, dur1 - args.duration)
    
    # Warn if transition might exceed lengths
    if args.offset + args.duration > dur1 or args.duration > dur2:
        print("⚠️ Warning: Transition duration exceeds available clip lengths. Output may be truncated or incomplete.")
    
    # FFmpeg command with xfade for video and acrossfade for audio
    filter_complex = (
        f"[0:v][1:v]xfade=transition={args.preset}:duration={args.duration}:offset={args.offset}[v];"
        f"[0:a][1:a]acrossfade=duration={args.duration}:offset={args.offset}[a]"
    )
    
    command = [
        "ffmpeg",
        "-i", str(args.input1),
        "-i", str(args.input2),
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",  # Use H.264 for compatibility
        "-c:a", "aac",      # Use AAC for audio compatibility
        "-b:v", "5000k",    # Set reasonable video bitrate
        str(clean_output)
    ]

    # Add -y flag if force overwrite is enabled
    run_ffmpeg_with_progress((command[:1] + ["-y"] + command[1:]) if args.force else command, args.input1, clean_output)