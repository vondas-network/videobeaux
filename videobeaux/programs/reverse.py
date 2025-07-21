from videobeaux.utils.ffmpeg_operations import run_ffmpeg_with_progress

def register_arguments(parser):
    parser.description = (
        "Reverses the video.oediv eht sesreveR"
    )
    print("✅ no additional arguments required")

def run(args):

    command = [
        "ffmpeg",
        "-y",
        "-i", args.input,
        "-vf", "reverse", 
        "-af", "areverse",
        args.output
    ]

    run_ffmpeg_with_progress((command[:1] + ["-y"] + command[1:]) if args.force else command, args.input, args.output)