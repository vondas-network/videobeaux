import typer
import yaml
from pathlib import Path

from programs import silence_extraction, resize, convert, extract_frames

config_file = Path(__file__).parent / "config.yaml"

def load_config():
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

config = load_config()

app = typer.Typer()

@app.command()
def silence_xtraction(
    min_d: int = typer.Option(None, help="Width of the output video"),
    max_d: int = typer.Option(None, help="Height of the output video"),
    adj: int = typer.Option(None, help="Height of the output video"),
    input_file: str = typer.Option(None, help="Input video file"),
    output_file: str = typer.Option(None, help="Output video file")
):
    params = { 
        "min_d": min_d,
        "max_d": max_d,
        "adj": adj,
        "input_file": input_file, 
        "output_file": output_file, 
        
    }
    defaults = config['silence_x']
    params = {key: params.get(key) or defaults[key] for key in defaults}

    silence_extraction.slncx_main(**params)

@app.command()
def resize_video(
    input_file: str = typer.Option(None, help="Input video file"),
    output_file: str = typer.Option(None, help="Output video file"),
    width: int = typer.Option(None, help="Width of the output video"),
    height: int = typer.Option(None, help="Height of the output video")
):
    """
    Resize a video to the given width and height.
    """
    params = { 
        "input_file": input_file, 
        "output_file": output_file, 
        "width": width, 
        "height": height 
    }
    defaults = config['resize']
    params = {key: params.get(key) or defaults[key] for key in defaults}

    resize.resize_video(**params)

@app.command()
def convert_video(
    input_file: str = typer.Option(None, help="Input video file"),
    output_file: str = typer.Option(None, help="Output video file"),
    format: str = typer.Option(None, help="Format of the output video")
):
    """
    Convert a video to a different format.
    """
    if not input_file:
        input_file = config['convert']['input_file']
    if not output_file:
        output_file = config['convert']['output_file']
    if not format:
        format = config['convert']['format']

    convert.convert_video(input_file, output_file, format)

@app.command()
def extract_frames(
    input_file: str = typer.Option(None, help="Input video file"),
    output_folder: str = typer.Option(None, help="Output folder for frames"),
    frame_rate: int = typer.Option(None, help="Frame rate for extracting frames")
):
    """
    Extract frames from a video at the specified frame rate.
    """
    if not input_file:
        input_file = config['extract_frames']['input_file']
    if not output_folder:
        output_folder = config['extract_frames']['output_folder']
    if not frame_rate:
        frame_rate = config['extract_frames']['frame_rate']

    extract_frames.extract_frames(input_file, output_folder, frame_rate)

if __name__ == "__main__":
    app()


'''def main():

    parser = argparse.ArgumentParser(description="VideoBeaux - It's You're Best Friend")
    subparsers = parser.add_subparsers(title='Subcommands', dest='command', help='Sub-command help')


    # Program selection
    #add_parser = subparsers.add_parser('program', help='Add a new task')
    #add_parser.add_argument('task', type=str, help='The task to add')

    # Project Management
    #prjmgmt_parser = subparsers.add_parser('project', help='Add a new task')
    #prjmgmt_parser.add_argument('--input_file', dest='infile', type=str, help='Full path to input file') # todo - use a path defined in config 
    #prjmgmt_parser.add_argument('--output_file', dest='outfile', type=str, help='filename of output file that will be save in videobeaux root dir') # todo - use a path defined in config 

    


    # Silence Xtraction
    silencextraction_parser = subparsers.add_parser('silence-xtraction', help='extracts silence from a given video')
    silencextraction_parser.add_argument('--min_d', dest='mind', type=int, help='Minimum duration of a silent chunk')
    silencextraction_parser.add_argument('--max_d', dest='maxd', type=int, help='Maximum duration of a silent chunk')
    silencextraction_parser.add_argument('--adj', dest='adj', type=int, help='Maximum duration of a silent chunk')
    silencextraction_parser.add_argument('--input_file', dest='infile', type=str, help='Full path to input file') # todo - use a path defined in config 
    silencextraction_parser.add_argument('--output_file', dest='outfile', type=str, help='filename of output file that will be save in videobeaux root dir') # todo - use a path defined in config 

    args = parser.parse_args()
    
    if args.command == 'silence-xtraction':
        silence_extraction.slncx_main(args.mind, args.maxd, args.adj, args.infile, args.outfile)

    else:
        parser.print_help()

'''
