import sys
from videogrep import parse_transcript, create_supercut


def silence_extraction(min_d, max_d, adj, input_file, output_file):
    print('DID WE MAKE IT^&(#(*&#(*&#(*&W#(*#&(*#&(*#&(*#&#*(&#))')
    print(input_file)
    # the min and max duration of silences to extract
    min_duration = min_d #0.1
    max_duration = max_d #1000.0

    # value to to trim off the end of each clip
    adjuster = adj #0.0

    filenames = input_file

    silences = []

    try:
        for filename in filenames:
            timestamps = parse_transcript(filename)

            words = []
            print(timestamps)
            for sentence in timestamps:
                words += sentence['words']

            for word1, word2 in zip(words[:-2], words[1:]):
                start = word1['end']
                end = word2['start'] - adjuster
                duration = end - start
                if duration > min_duration and duration < max_duration:
                    silences.append({'start': start, 'end': end, 'file': filename})

        create_supercut(silences, f"{output_file}.mp4")
        return "ok"
    except Exception as e:
        print(e)
        return e