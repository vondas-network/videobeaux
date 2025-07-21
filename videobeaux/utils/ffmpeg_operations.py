import subprocess
import re
from tqdm import tqdm
from pathlib import Path

def get_video_duration(input_file):
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            input_file
        ],
        capture_output=True,
        text=True
    )
    return float(result.stdout.strip())

def time_to_seconds(h, m, s):
    return int(h) * 3600 + int(m) * 60 + float(s)

def run_ffmpeg_with_progress(command, input_file, output_file, show_ffmpeg_output=False):
    duration = get_video_duration(input_file)
    print(f"Input duration: {duration:.2f} seconds")
    output_idx = len(command) - 1
    command = command[:output_idx] + ["-progress", "pipe:1"] + command[output_idx:]
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE if show_ffmpeg_output else subprocess.DEVNULL,
        bufsize=1,
        universal_newlines=True
    )
    pbar = tqdm(
        total=duration,
        unit="s",
        dynamic_ncols=True,
        bar_format="{l_bar}{bar} | {n:.2f}/{total:.2f}s [{elapsed}<{remaining}]"
    )
    pbar.set_description(f"🔨 Processing {Path(input_file).name}")

    try:
        out_time_re = re.compile(r"out_time=(\d+):(\d+):(\d+\.\d+)")

        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break

            line = line.strip()
            match = out_time_re.match(line)
            if match:
                elapsed = time_to_seconds(*match.groups())
                increment = elapsed - pbar.n
                if increment > 0:
                    increment = min(increment, duration - pbar.n)
                    pbar.update(increment)

            elif line == "progress=end":
                break

        process.wait()
        remaining = duration - pbar.n
        if remaining > 0:
            pbar.update(remaining)
        pbar.close()

        if process.returncode != 0:
            raise RuntimeError(f"❌ ffmpeg exited with code {process.returncode}")
        
        print(f"\n📺 Process Complete: {output_file} \n")

    except Exception as e:
        pbar.close()
        process.kill()
        raise e

def run_ffmpeg_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")