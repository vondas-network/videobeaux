from videobeaux.utils.ffmpeg_operations import run_ffmpeg_with_progress

def register_arguments(parser):
    parser.description = (
        "Akin to repainting the same image while smudged with alcohol."
    )
    parser.add_argument(
        "--new_height",
        required=True,
        type=str,
        help="Height, in pixels of the desiered resized --output video."
    )
    parser.add_argument(
        "--new_width",
        required=True,
        type=str,
        help="Width, in pixels of the desiered resized --output video."
    )

def run(args):

    command = [
        "ffmpeg",
        "-i", args.input,
        "-vf", f"scale={args.new_width}:{args.new_height}",
        args.output
    ]

    run_ffmpeg_with_progress((command[:1] + ["-y"] + command[1:]) if args.force else command, args.input, args.output)