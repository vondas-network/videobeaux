import typer
from typing_extensions import Annotated

# NEW
import os 
import calendar
 

from pathlib import Path

from programs import (
    blur_pix,
    broken_scroll,
    convert, 
    download_yt,
    extract_frames, 
    extract_sound, 
    frame_delay_pro1,
    frame_delay_pro2,
    lsd_feedback,
    mirror_delay,
    nostalgic_stutter,
    num_edits,
    overexposed_stutter,
    resize, 
    reverse,
    scrolling_pro,
    silence_xtraction,    
    speed,
    stack_2x,    
    stutter_pro,
    transcraibe)

from utils import load_config
from datetime import datetime

from pyfiglet import Figlet
a = Figlet(font='ogre')
print(a.renderText("videobeaux"))
print("Your friendly multilateral video toolkit built for artists by artists.")
print("It's your best friend.")
print('-' * 50)

config = load_config.load_config()

proj_mgmt_config = config['proj_mgmt']
v_ext = proj_mgmt_config['default_video_file_ext']
a_ext = proj_mgmt_config['default_audio_file_ext']

now = datetime.now()
ct = now.strftime("%Y-%m-%d_%H-%M-%S")

app = typer.Typer()


##########
# yt-dlp
##########
@app.command('download-yt', help='Downloads the provided link with yt-dlp')
def yt_dlp_vb(
    yt_url: str = typer.Argument(None, help="URL of the YT video"),
    output_file: str = typer.Argument(None, help="Width of the output video"),
    format: str = typer.Argument(v_ext, help="Width of the output video"),
):
    params = { 
        "yt_url": yt_url,
        "output_file": output_file,  
        "format": format
    }
    defaults = config['download_yt']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    download_yt.download_yt(**params)


###############
# transcraibe
###############
@app.command('transcraibe', help='Transcribes the video with ai (vosk) - transcrAIbe')
def transcraibe_vb(
    input_file: str = typer.Argument(None, help='Video file you would like to transcribe.'),
    stt_model: str = typer.Argument(None, help="URL of the YT video")
):
    params = { 
        "input_file": input_file,
        "stt_model": stt_model
    }
    defaults = config['transcraibe']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    transcraibe.vosk_stt(**params)


#####################
# silence-xtraction
#####################
@app.command('silence-xtraction', help="Stitches togehter video chunks that have no discernable words." +
              "This does NOT use audio analysis, but instead identifes the presence of a 'word' using the .srt transcription file")
def silence_xtraction_vb(
    min_d: int = typer.Argument(None, help="Minimum duration of a chunk of silence."),
    max_d: int = typer.Argument(None, help="Maximum duration of a chunk of silence."),
    adj: int = typer.Argument(None, help="Adjustment value"),
    input_file: str = typer.Argument(None, help="Input video file"),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "min_d": min_d,
        "max_d": max_d,
        "adj": adj,
        "input_file": input_file, 
        "output_file": output_file,
    }

    defaults = config['silence_x']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    silence_xtraction.silence_xtraction(**params)


##########
# resize 
##########
@app.command('resize', help='Resize a video to the given width and height.')
def resize_vb(
    input_file: str = typer.Argument(None, help="Input video file"),
    output_file: str = typer.Argument(None, help="Output video file"),
    width: int = typer.Argument(None, help="Width of the output video"),
    height: int = typer.Argument(None, help="Height of the output video")
):
    params = { 
        "input_file": input_file, 
        "output_file": output_file, 
        "width": width, 
        "height": height 
    }
    defaults = config['resize']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    resize.resize(**params)


###########
# convert
###########
@app.command('convert', help='Convert a video to a different format.')
def convert_vb(
    input_file: str = typer.Argument(None, help="Input video file"),
    output_file: str = typer.Argument(None, help="Output video file"),
    format: str = typer.Argument(None, help="Format of the output video")
):
    params = { 
        "input_file": input_file, 
        "output_file": output_file, 
        "format": format
    }
    defaults = config['convert']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    convert.convert(**params)


##################
# extract-frames
##################
@app.command('extract-frames', help='Extract frames from a video at the specified frame rate.')
def extract_frames_vb(
    input_file: str = typer.Argument(None, help="Input video file"),
    output_file: str = typer.Argument(None, help="Output folder for frames"),
    frame_rate: int = typer.Argument(None, help="Frame rate for extracting frames")
):
    params = { 
        "input_file": input_file, 
        "output_file": output_file, 
        "frame_rate": frame_rate
    }
    defaults = config['extract_frames']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    extract_frames.extract_frames(**params)


#################
# extract-sound
#################
@app.command('extract-sound', help='Extract audio from video file.')
def extract_sound_vb(
    input_file: str = typer.Argument(None, help="Input video file"),
    output_file: str = typer.Argument(None, help="Output audio file")
):
    params = { 
        "input_file": input_file, 
        "output_file": output_file
    }
    defaults = config['extract_sound']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    print(params)
    extract_sound.extract_sound(**params)



###########
# reverse
###########
@app.command('reverse', help='Reverse video file.')
def reverse_vb(
    input_file: str = typer.Argument(None, help="Input video file"),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file, 
        "output_file": output_file
    }
    defaults = config['reverse']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    reverse.reverse(**params)


############
# stack-2x
############
@app.command('stack-2x', help='Stack 2 videos on top of each other keeping the original orientation.')
def stack_2x_vb(
    input_file1: str = typer.Argument(None, help="Input video file 1"),
    input_file2: str = typer.Argument(None, help="Input video file 2"),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file1": input_file1,
        "input_file2": input_file2, 
        "output_file": output_file
    }
    defaults = config['stack_2x']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    stack_2x.stack_2x(**params)


################
# lsd-feedback
################
@app.command('lsd-feedback', help='Apply LSD feedback effect to video file.')
def lsd_feedback_vb(
    input_file: str = typer.Argument(None, help="Input video file "),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['lsd_feedback']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    lsd_feedback.lsd_feedback(**params)

################
# num-edits
################
@app.command('num-edits', help='Apply LSD feedback effect to video file.')
def num_edits_vb(
    input_file: str = typer.Argument(None, help="Input video file "),
    count: str = typer.Argument(None, help="Input video file "),
    output_file: str = typer.Argument(None, help="Input video file ")
):
    params = { 
        "input_file": input_file,
        "count": count,
        "output_file": output_file
    }
    defaults = config['num_edits']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    num_edits.num_edits(**params)


#####################
# nostalgic-stutter
#####################
@app.command('nostalgic-stutter', help='Apply nostaglic stutter effect to video file.')
def nostalgic_stutter_vb(
    input_file: str = typer.Argument(None, help="Input video file"),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['nostalgic_stutter']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    nostalgic_stutter.nostalgic_stutter(**params)


####################
# frame-delay-pro1
####################
@app.command('frame-delay-pro1', help='Apply the pro1 frame delay to video file.')
def frame_delay_pro1_vb(
    input_file: str = typer.Argument(None, help="Input video file "),
    num_of_frames: int = typer.Argument(None, help="Input weight for frame delay"),    
    frame_weights: str = typer.Argument(None, help="Input weight for frame delay"),    
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "num_of_frames": num_of_frames,
        "frame_weights": frame_weights,
        "output_file": output_file
    }
    defaults = config['frame_delay_pro1']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    frame_delay_pro1.frame_delay_pro1(**params)


####################
# frame-delay-pro2
####################
@app.command('frame-delay-pro2', help='Apply the pro2 frame delay to video file.')
def frame_delay_pro2_vb(
    input_file: str = typer.Argument(None, help="Input video file "),
    decay: int = typer.Argument(None, help=""),    
    planes: str = typer.Argument(None, help="Input weight for frame delay"),    
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "decay": decay,
        "planes": planes,
        "output_file": output_file
    }
    defaults = config['frame_delay_pro2']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    frame_delay_pro2.frame_delay_pro2(**params)


################
# mirror-delay
################
@app.command('mirror-delay', help='Apply mirrored delay effect to video file.')
def mirror_delay_vb(
    input_file: str = typer.Argument(None, help="Input video file"), 
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['mirror_delay']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    print(params)
    mirror_delay.mirror_delay(**params)


######################
# overexposed-stutter
######################
@app.command('overexposed-stutter', help='Apply overexposed stutter effect to video file.')
def overexposed_stutter_vb(
    input_file: str = typer.Argument(None, help="Input video file"), 
    output_file: str = typer.Argument(None, help="Output video file")
):

    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['overexposed_stutter']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    overexposed_stutter.overexposed_stutter(**params)


###############
# stutter-pro
###############
@app.command('stutter-pro', help='Apply stutter pro effect to video file.')
def stutter_pro_vb(
    input_file: str = typer.Argument(None, help="Input video file"), 
    stutter: str = typer.Argument(None, help="Frame stutter parameter"), 
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "stutter": stutter,
        "output_file": output_file
    }
    defaults = config['stutter_pro']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    stutter_pro.stutter_pro(**params)

#############
# speed
#############
@app.command('speed', help='Apply speed effect to video file.')
def speed_vb(
    input_file: str = typer.Argument(None, help="Input video file"), 
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['speed']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    speed.speed(**params)

#############
# broken_scroll
#############
@app.command('broken-scroll', help='Apply broken_scroll effect to video file.')
def broken_scroll_vb(
    input_file: str = typer.Argument(None, help="Input video file"), 
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['broken_scroll']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    broken_scroll.broken_scroll(**params)


#################
# scrolling-pro
#################
@app.command('scrolling-pro', help='Apply scrolling pro effect to video file.')
def scrolling_pro_video(
    input_file: str = typer.Argument(None, help="Input video file"), 
    horizontal: str = typer.Argument(None, help="Horizontal scroll parameter"), 
    vertical: str = typer.Argument(None, help="Vertical scroll parameter"), 
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "horizontal": horizontal,
        "verticla": vertical,
        "output_file": output_file
    }
    defaults = config['scrolling_pro']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    scrolling_pro.scrolling_pro(**params)

############
# blur-pix
############
@app.command('blur-pix', help='Apply blur pix effect to video file.')
def blur_pix_video(
    input_file: str = typer.Argument(None, help="Input video file"), 
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['blur_pix']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    blur_pix.blur_pix(**params)

if __name__ == "__main__":
    app()

