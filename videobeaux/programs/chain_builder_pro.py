import importlib
import argparse
import json
import tempfile
import shutil
from pathlib import Path
from types import SimpleNamespace

def register_arguments(parser):
    parser.description = (
        "The output of the first will be used as the input for the next, and so on. \n"
        "Only supports program modes that do not require their own specific arguments."
    )

    parser.add_argument(
        "--chain_config",
        required=True,
        type=str,
        help=(
            "Path to the chain_config.json file"
        )
    )

def run(args):
    chain_path = Path(args.chain_config)
    if not chain_path.exists():
        raise FileNotFoundError(f"Chain config file not found: {chain_path}")

    with open(chain_path) as f:
        chain = json.load(f)

    tmp_dir = Path(tempfile.mkdtemp(prefix="videobeaux_chain_"))
    current_input = Path(args.input)

    try:
        for i, step in enumerate(chain):
            prog_name = step["program"]
            step_args_dict = step.get("args", {})
            step_args_dict['force'] = args.force
            module = importlib.import_module(f"videobeaux.programs.{prog_name}")
            intermediate_output = tmp_dir / f"step_{i}_{prog_name}.mp4"

            # Merge global args with step-specific args
            merged_args = {
                "input": str(current_input),
                "output": str(intermediate_output),
                **step_args_dict
            }

            # Include other global args if needed (e.g., verbosity)
            final_args = argparse.Namespace(**merged_args)

            print(f"🔁 [{i+1}/{len(chain)}] Running: {prog_name} with args: {step_args_dict}")
            try:
                module.run(final_args)
            except Exception as e:
                print(e)

            current_input = intermediate_output

        # Move final result to target output
        final_output = Path(args.output)
        shutil.move(current_input, final_output)
        print(f"✅ Final output written to {final_output}")

    finally:
        shutil.rmtree(tmp_dir)