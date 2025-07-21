import yt_dlp
# yt_dlp is dope, but the docs for the python module suck. 
# they say "oh, just read the official yt-dlp docs and it should just work"
# but, while the logic is the same, the param format is not exact
# for example - to include a subtitle file in the download via the yt-dlp cli tool, yt-dlp docs say to use --write-auto-subs
# but, the same option here is writeautomaticsub for no discernable reason
# dm us if you know why
# in the meantime, you need to check the source code AND the docs to use certain options

# https://pypi.org/project/yt-dlp/
# https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py#L181

def register_arguments(parser):
    parser.description = (
            "downloads the yt video url provided in the --input arg as mp4. \n"
            "--output just takes a filename"
    )

def run(args):
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': f"{args.output}", #https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#output-template
        "writeautomaticsub":True # will include a vtt file. note: this won't work for some videobeaux functions that require an srt from vosk
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(args.input)
    
