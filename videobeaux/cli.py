import argparse
import importlib
import sys
from pathlib import Path
from pyfiglet import Figlet

from videobeaux.utils.vb_argparser import VB_Program_ArgParser

def main():
    a = Figlet(font='ogre')
    print(a.renderText("videobeaux"))
    print("Your friendly multilateral video toolkit built for artists by artists. \nhttps://vondas.software")
    print('-' * 50)

    # global parser
    parser = argparse.ArgumentParser(
        description="📺 Your friendly multilateral video toolkit built for artists by artists. \n It's your best friend! \nhttps://vondas.software",
        usage="python3 -m videobeaux.cli --program PROGRAM [global options] [program options]",
        add_help=False,
        formatter_class=argparse.RawTextHelpFormatter
      # Let us handle --help manually
    )
    parser.add_argument("-P", "--program", help="Name of the effect program to run (e.g. convert, glitch)")
    parser.add_argument("-i", "--input", help="Input video file - mp4 only")
    parser.add_argument("-o", "--output", help="Output file name, no extension. Output will be saved as mp4.")
    #parser.add_argument("-c", "--config", help="Optional config file")
    parser.add_argument("-F", "--force", action="store_true", help="Force overwrite output file")
    parser.add_argument("-h", "--help", action="store_true", help="Show help message and exit")

    global_args, remaining = parser.parse_known_args()

    # Validate and sanitize output filename
    if global_args.output:
        output_path = Path(global_args.output)
        suffix = output_path.suffix.lower()

        if suffix and suffix != ".mp4":
            print(f"❌ Invalid file extension.  --output accepts a file name, which will be saved as mp4.")
            sys.exit(1)
        if not suffix:
            global_args.output += ".mp4"


    # gloabl --help
    if global_args.help and not global_args.program:
        parser.print_help()
        sys.exit(0)

    # program load
    if not global_args.program:
        print("❌ You must specify a --program.")
        parser.print_help()
        sys.exit(1)
    try:
        mod = importlib.import_module(f"videobeaux.programs.{global_args.program}")
        print(f"Selected program mode: {global_args.program}")

    except ModuleNotFoundError as e:
        print(f"❌ Program '{global_args.program}' not found in videobeaux.programs. ({e.name})")
        sys.exit(1)

    program_parser = VB_Program_ArgParser(
        prog=f"{parser.prog} --program {global_args.program}",
        description=f"🔧 Arguments for program '{global_args.program}'",
        formatter_class=argparse.RawTextHelpFormatter
    )
    mod.register_arguments(program_parser)


    # program --help
    if global_args.help:
        parser.print_help()
        print("\n 👁️ 👇 Additional help for program mode 👇 👁️")
        program_parser.print_help()
        sys.exit(0)

    program_args = program_parser.parse_args(remaining)
    if global_args.input and not Path(global_args.input).exists():
        print(f"❌ {global_args.input} doesn't exists. WTF?")
        sys.exit(1)

    if global_args.output and not global_args.force and Path(global_args.output).exists():
        print(f"❌ {global_args.output} already exists. Use --force to overwrite.")
        sys.exit(1)

    combined_args = argparse.Namespace(**vars(global_args), **vars(program_args))
    try:
        mod.run(combined_args)
    except:
        print(f"😵 Exiting due to failure...")
        sys.exit(1)

if __name__ == "__main__":
    main()
