from videobeaux.utils.ffmpeg_operations import run_ffmpeg_with_progress

def register_arguments(parser):
    parser.description = (
        "Makes the video seem like a dream when you are sick with a bug."
    )
    parser.add_argument(
        "-fq", "--frame_quantity",
        required=True,
        type=str,
        help="Number of past frames to retain to control length of visual memory trail."
        
    )
    parser.add_argument(
        "-fw", "--frame_weights",
        required=True,
        type=str,
        help="Value between 0.0 and 1.0. How much influence each retained frame has when blended into the output."
    )

def run(args):
    command = [
        "ffmpeg",
        "-i", args.input,
        "-vf", f"tmix=frames={args.frame_quantity}:weights='{args.frame_weights}'",
        "-c:v", "libx264",
        "-crf", "23",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ac", "2",
        args.output
    ]

    run_ffmpeg_with_progress((command[:1] + ["-y"] + command[1:]) if args.force else command, args.input, args.output)
