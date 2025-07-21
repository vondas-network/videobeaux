import os
import json
import time
import subprocess
import imageio_ffmpeg
from vosk import Model, KaldiRecognizer, SetLogLevel
from pathlib import Path
import sys

def register_arguments(parser):
    parser.add_argument(
        "-m", "--stt_model",
        required=True,
        type=str,
        help="The file path to the vosk model being used. \n"
        "Transcriptions will be saved with the same filename as the input video file, in the same directory.  as the input file. \n"
        "This is to ensure compatibilty with other program modes that rely on the transcription. \n"
        "--output is required for every program mode, but will be ignored here."
        )

# this piece is pulled almost verbatim from videogrep
# maybe we could have just used subprocess and run videogrep --transcribe since it is already a dependancy
# but it is here for archival purposes
# big up to Sam Levigne aka antiboredom 
# https://github.com/antiboredom/videogrep

def run(args):
    if args.output:
        print("📢 NOTE: --output is required, but will be ignored. see transcraibe --help for more info. \n ")
    MAX_CHARS = 36

    start_time = time.time()

    transcript_file = os.path.splitext(args.input)[0] + ".json"

    if os.path.exists(transcript_file):
        print(f"Transcription file '{transcript_file}' already exists")
        sys.exit(1)


    if not os.path.exists(args.input):
        print("Could not find file", args.input)
        return []

    _model_path: str = 'defaultmodel'

    if args.stt_model is not None:
        _model_path = args.stt_model

    if not os.path.exists(_model_path):
        print("Could not find model folder")
        exit(1)

    print("Transcribing", args.input)
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
            args.input,
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
        print("No words found.")
        return []

    with open(transcript_file, "w", encoding="utf-8") as outfile:
        json.dump(out, outfile)
    
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Transcription took: {execution_time} seconds")

    #return out
    return [] 