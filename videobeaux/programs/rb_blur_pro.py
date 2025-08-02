from videobeaux.utils.ffmpeg_operations import run_ffmpeg_with_progress

def register_arguments(parser):
    parser.description = (
        "Filter to reduce color banding in flat, gradient-heavy areas (e.g., skies, shadows)."
    )

    parser.add_argument(
        "--strength",
        required=True,
        type=str,
        help=(
            ""
        )
    )

    parser.add_argument(
        "--radius",
        required=True,
        type=str,
        help=(
            ""
        )
    )

def run(args):

    command = [
        "ffmpeg",
        "-i", args.input,
        "-filter_complex", f"[0:v]gradfun=strength={args.strength}:radius={args.radius}[out_v]",
        "-map", "[out_v]",
        "-map", "0:a",
        args.output
    ]

    run_ffmpeg_with_progress((command[:1] + ["-y"] + command[1:]) if args.force else command, args.input, args.output)