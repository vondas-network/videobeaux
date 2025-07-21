from videobeaux.utils.ffmpeg_operations import run_ffmpeg_with_progress
from videogrep import parse_transcript, create_supercut
import sys

def register_arguments(parser):
    parser.description = (
        "A trnscription .json of the same name, and in the same dir as --input. \n"
        "See --program transcraibe --help and vosk docs"
        "Identifes instances of speech, per the transcript timestamps, and removes those portions of the video. \n"
        "The output will be what's left. Not exactly silence, but no discernable words."
    )
    parser.add_argument(
        "--min_d",
        required=True,
        type=float,
        help=(
            "Minimum duration (in seconds) of a silence to consider."
        )
    )
    parser.add_argument(
        "--max_d",
        required=True,
        type=float,
        help=(
            "Maximum duration (in seconds) of a silence to consider."
        )
    )
    parser.add_argument(
        "--adjuster",
        required=True,
        type=float,
        help=(
            "Adjustment offset (seconds) to shorten the silence from the end."
            "Anecdotally, the closer to 0, the more gutteral speech non-word sounds are included."
        )
    )

def run(args):
    filename = args.input
    silences = []
    try:
        timestamps = parse_transcript(filename)
        words = []
        for sentence in timestamps:
            words += sentence['words']
        for word1, word2 in zip(words[:-2], words[1:]):
            start = word1['end']            
            end = word2['start'] - args.adjuster
            duration = end - start
            if duration > args.min_d and duration < args.max_d:
                silences.append({'start': start, 'end': end, 'file': filename})

        try:
            create_supercut(silences, f"{args.output}")
        except Exception as e:
            print(e)
      
    except Exception as e:
        print("Videogrep exception likely...")
        print(e)
        return e