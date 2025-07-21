from videobeaux.utils.ffmpeg_operations import run_ffmpeg_with_progress

def register_arguments(parser):
    parser.description = (
        "Overlay an image with location & dimension control."
    )
    parser.add_argument(
        "--overlay_img",
        required=True,
        type=str,
        help="Path to the file of the image you want overlayed onto the video."
        
    )
    parser.add_argument(
        "--x_pos",
        required=True,
        type=str,
        help="Horizontal position, in pixels, of the top left corner of the overlay image."
    )
    parser.add_argument(
        "--y_pos",
        required=True,
        type=str,
        help="Vertical position, in pixels, of the top left corner of the overlay image."
    )
    parser.add_argument(
        "--img_height",
        required=True,
        type=str,
        help="Height, in pixels, of the image being overlayed."
    )
    parser.add_argument(
        "--img_width",
        required=True,
        type=str,
        help="Width, in pixels, of the image being overlayed."
    )

def run(args):
    command = [
        "ffmpeg",
        "-i", args.input,
        "-i", args.overlay_img,
        "-filter_complex",  f"[1:v]scale={args.img_width}:{args.img_height}[ovr];[0:v][ovr]overlay={args.x_pos}:{args.y_pos}",
        "-map", "0:a",
        args.output 
    ]

    run_ffmpeg_with_progress((command[:1] + ["-y"] + command[1:]) if args.force else command, args.input, args.output)
