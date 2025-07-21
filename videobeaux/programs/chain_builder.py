from pathlib import Path
import importlib
import tempfile
import argparse
import shutil
import sys

def register_arguments(parser):
    parser.description = (
        "The output of the first will be used as the input for the next, and so on. \n"
        "Only supports program modes that do not require their own specific arguments."
    )

    parser.add_argument(
        "--chain",
        required=True,
        type=str,
        help=(
            "A comma separated list of programs to run."
        )
    )

def run(args):
    chain = args.chain.split(",") if args.chain else []
    if not chain:
        raise ValueError("Chain must include at least one program name, e.g. --chain stutter,blur")
    input_path = Path(args.input)
    current_input = input_path
    tmp_dir = Path(tempfile.mkdtemp(prefix="videobeaux_chain_"))
    try:
        for i, prog_name in enumerate(chain):
            module = importlib.import_module(f"videobeaux.programs.{prog_name}")
            intermediate_output = tmp_dir / f"step_{i}_{prog_name}.mp4"
            step_args = args.__dict__.copy()
            step_args["input"] = str(current_input)
            step_args["output"] = str(intermediate_output)
            step_args = argparse.Namespace(**step_args)
            # print(step_args)
            print(f"🔁 Running step {i + 1}/{len(chain)}: {prog_name}")
            try:
                module.run(step_args)
            except Exception as e:
                print(f"❌ {prog_name} requires additional args and cannot be chained.")
                shutil.rmtree(tmp_dir)
                sys.exit(1)
            current_input = intermediate_output

        final_output = Path(args.output)
        shutil.move(current_input, final_output)
        print(f"✅ Final output written to {final_output}")
    except Exception as e:
        print(e)
    finally:
        shutil.rmtree(tmp_dir)
