from videobeaux.utils.ffmpeg_operations import run_ffmpeg_with_progress

def register_arguments(parser):
    parser.description = (
        "Apply filter from the perspective of a zombie on TC-1 hallucinogens."
    )

    parser.add_argument(
        "--radius",
        required=True,
        type=str,
        help=(
            ""
        )
    )

    parser.add_argument(
        "--factor",
        required=True,
        type=str,
        help=(
            ""
        )
    )

    parser.add_argument(
        "--blend",
        required=True,
        type=str,
        help=(
            ""
        )
    )

    parser.add_argument(
        "--similarity",
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
        "-filter_complex", f"[0:v]amplify=radius={args.radius}:factor={args.factor},chromakey=color=blue:similarity={args.similarity}:blend={args.blend}[out_v]",
        "-map", "[out_v]",
        "-map", "0:a",
        "-c:v", "libx264",
        "-profile:v", "main",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        args.output
    ]

    run_ffmpeg_with_progress((command[:1] + ["-y"] + command[1:]) if args.force else command, args.input, args.output)

