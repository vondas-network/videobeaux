from videobeaux.utils.ffmpeg_operations import run_ffmpeg_with_progress

def register_arguments(parser):
    parser.description = (
        "Apply video looper effect base on frame size & start frame."

    )
    parser.add_argument(
        "--size_in_frames",
        required=True,
        type=str,
        help="The number of frames in the segment to loop."
        
    )
    parser.add_argument(
        "--loop_count",
        required=True,
        type=str,
        help=(
            "Number of additional times to repeat the segment. \n"
            "2 means the segment appears 3 times total (original + 2 repeats)."
        )
    )
    parser.add_argument(
        "--start_frame",
        required=True,
        type=str,
        help=(
            "The starting frame number in the video where the segment begins."
        )
    )
    
def run(args):
    command = [
        "ffmpeg",
        "-i", args.input,
        "-filter_complex", f"[0:v]loop=loop={args.loop_count}:size={args.size_in_frames}:start={args.start_frame}[out_v]",
        "-map", "[out_v]",
        args.output
    ]

    run_ffmpeg_with_progress((command[:1] + ["-y"] + command[1:]) if args.force else command, args.input, args.output)