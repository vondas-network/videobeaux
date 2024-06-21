import os
import json
import time
import subprocess
import imageio_ffmpeg
from glob import glob
from subprocess import run
from vosk import Model, KaldiRecognizer, SetLogLevel

import yaml
from pathlib import Path

config_file = Path(__file__).parent.parent / "config.yaml"
def load_config():
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)
config = load_config()
proj_mgmt_config = config['proj_mgmt']

# this piece is pulled almost verbatim from videogrep
# maybe we could have just used subprocess and run videogrep --transcribe since it is already a dependancy
# but it is here for archival purposes
# big up to Sam Levigne aka antiboredom 
# https://github.com/antiboredom/videogrep
def vosk_stt(input_file, stt_model):
    if stt_model is None:
        stt_model = proj_mgmt_config['stt_model']
    MAX_CHARS = 36

    start_time = time.time()

    transcript_file = os.path.splitext(input_file)[0] + ".json"

    if os.path.exists(transcript_file):
        with open(transcript_file, "r") as infile:
            data = json.load(infile)
        return data

    if not os.path.exists(input_file):
        print("Could not find file", input_file)
        return []

    _model_path: str = 'defaultmodel'

    if stt_model is not None:
        _model_path = stt_model

    if not os.path.exists(_model_path):
        print("Could not find model folder")
        exit(1)

    print("Transcribing", input_file)
    SetLogLevel(-1)

    sample_rate = 16000
    model = Model(_model_path)
    rec = KaldiRecognizer(model, sample_rate)
    rec.SetWords(True)

    process = subprocess.Popen(
        [
            imageio_ffmpeg.get_ffmpeg_exe(),
            "-nostdin",
            "-loglevel",
            "quiet",
            "-i",
            input_file,
            "-ar",
            str(sample_rate),
            "-ac",
            "1",
            "-f",
            "s16le",
            "-",
        ],
        stdout=subprocess.PIPE,
    )

    tot_samples = 0
    result = []
    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            tot_samples += len(data)
            result.append(json.loads(rec.Result()))
    result.append(json.loads(rec.FinalResult()))

    out = []
    for r in result:
        if "result" not in r:
            continue
        words = [w for w in r["result"]]
        item = {"content": "", "start": None, "end": None, "words": []}
        for w in words:
            item["content"] += w["word"] + " "
            item["words"].append(w)
            if len(item["content"]) > MAX_CHARS or w == words[-1]:
                item["content"] = item["content"].strip()
                item["start"] = item["words"][0]["start"]
                item["end"] = item["words"][-1]["end"]
                out.append(item)
                item = {"content": "", "start": None, "end": None, "words": []}

    if len(out) == 0:
        print("No words found in", i)
        return []

    with open(transcript_file, "w", encoding="utf-8") as outfile:
        json.dump(out, outfile)
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Transcription took: {execution_time} seconds")

    #return out
    return [] 