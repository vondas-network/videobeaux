from videobeaux.utils.ffmpeg_operations import run_ffmpeg_with_progress

def register_arguments(parser):
    parser.description = (
        "Makes the video seem like a dream when you are sick with a bug."
    )
    parser.add_argument(
        "-d", "--decay",
        required=True,
        type=str,
        help="Value between 0.0 and 1.0. Controls how quickly the trail fades. "
        
    )
    parser.add_argument(
        "-pl", "--planes",
        required=True,
        type=str,
        help=(
            "Value is a bitmask (0–7) for YUV planes. \n"
            "0 = no effect \n"
            "1 = Y (luma/brightness) \n"
            "2 = U (blue chroma) \n"
            "3 = Y + U	Brightness + blue projection \n"
            "4 = V (red chroma) \n"
            "5 = Y + V	Brightness + red projection \n"
            "6 - U + V	Full color, but not brightness \n"
            "7 - Y + U + V	Affects everything (full color trail)"
        )
    )


def run(args):
    command = [
        "ffmpeg",
        "-i", args.input,
        "-vf", f"format=yuv420p,lagfun=decay={args.decay}:planes={args.planes}",
        args.output
    ]

    run_ffmpeg_with_progress((command[:1] + ["-y"] + command[1:]) if args.force else command, args.input, args.output)
