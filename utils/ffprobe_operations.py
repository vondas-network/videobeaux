import subprocess

def run_ffprobe_command(command):
    try:
        result = subprocess.run(command, check=True, capture_output=True)
        # print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")