import os 
import typer
import calendar
from pathlib import Path
from typing_extensions import Annotated 

from programs import (
    bad_animation,
    bad_contrast,
    bad_predator,
    ball_point_pen,
    septic,
    blur_pix,
    broken_scroll,
    convert,
    digital_boss,
    double_cup,
    download_yt,
    extract_frames, 
    extract_sound, 
    fever,
    frame_delay_pro1,
    frame_delay_pro2,
    ghostee,
    light_snow,
    looper_pro,
    lsd_feedback,
    mirror_delay,
    nostalgic_stutter,
    num_edits,
    overexposed_stutter,
    overlay_img_pro,
    pickle_juice,
    rb_blur,
    recalled_sensor,
    repainting,
    resize, 
    reverse,
    scrolling_pro,
    silence_xtraction,    
    slight_smear,
    smudge,
    soapblind,
    speed,
    splitting,
    stack_2x, 
    steel_wash,   
    stutter_pro,
    t1000,
    transcraibe,
    twociz,
    wbflare,
    xrgb,
    zapruder)

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

######################
# bad_animation
######################
@app.command('bad_animation', help='Apply a bad animation effect.')
def bad_animation_vb(
    input_file: str = typer.Argument(None, help="Input video file"), 
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['bad_animation']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    bad_animation.bad_animation(**params)

######################
# bad_contrast
######################
@app.command('bad_contrast', help='Apply a bad constrast effect.')
def bad_contrast_vb(
    input_file: str = typer.Argument(None, help="Input video file"), 
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['bad_contrast']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    bad_contrast.bad_contrast(**params)

######################
# ball_point_pen
######################
@app.command('ball_point_pen', help='Apply a ball point pen effect.')
def ball_point_pen_vb(
    input_file: str = typer.Argument(None, help="Input video file"), 
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['ball_point_pen']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    ball_point_pen.ball_point_pen(**params)

######################
# bad_predator
######################
@app.command('bad_predator', help='Apply bad Predator heat vision effect to video file.')
def bad_predator_vb(
    input_file: str = typer.Argument(None, help="Input video file"), 
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file1": input_file,
        "output_file": output_file
    }
    defaults = config['bad_predator']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    bad_predator.bad_predator(**params)

######################
# blur_pix
######################
@app.command('blur_pix', help='Apply blur pix effect to video file.')
def blur_pix_vb(
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

######################
# broken_scroll
######################
@app.command('broken_scroll', help='Apply broken_scroll effect to video file.')
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

######################
# convert
######################
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

######################
# digital_boss
######################
@app.command('digital_boss', help='Apply fever effect to video.')
def digital_boss_vb(
    input_file: str = typer.Argument(None, help="Input video file"),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file, 
        "output_file": output_file
    }
    defaults = config['digital_boss']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    digital_boss.digital_boss(**params)   

######################
# fever
######################
@app.command('fever', help='Apply fever effect to video.')
def fever_vb(
    input_file: str = typer.Argument(None, help="Input video file"),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file, 
        "output_file": output_file
    }
    defaults = config['fever']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    fever.fever(**params)   

######################
# double_cup
######################
@app.command('double_cup', help='Apply the effect of purple drank.')
def double_cup_vb(
    input_file: str = typer.Argument(None, help="Input video file"),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file, 
        "output_file": output_file
    }
    defaults = config['double_cup']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    double_cup.double_cup(**params)    

######################
# download_yt : yt-dlp 
######################
@app.command('download_yt', help='Downloads the provided link with yt-dlp')
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

######################
# extract_frames
######################
@app.command('extract_frames', help='Extract frames from a video at the specified frame rate.')
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

######################
# extract_sound
######################
@app.command('extract_sound', help='Extract audio from video file.')
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

######################
# frame_delay_pro1
######################
@app.command('frame_delay_pro1', help='Apply the pro1 frame delay to video file.')
def frame_delay_pro1_vb(
    input_file: str = typer.Argument(None, help="Input video file "),
    output_file: str = typer.Argument(None, help="Output video file"),
    num_of_frames: int = typer.Argument(None, help="Input weight for frame delay"),    
    frame_weights: str = typer.Argument(None, help="Input weight for frame delay")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file,
        "num_of_frames": num_of_frames,
        "frame_weights": frame_weights
    }
    defaults = config['frame_delay_pro1']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    frame_delay_pro1.frame_delay_pro1(**params)

######################
# frame_delay_pro2
######################
@app.command('frame_delay_pro2', help='Apply the pro2 frame delay to video file.')
def frame_delay_pro2_vb(
    input_file: str = typer.Argument(None, help="Input video file "),
    output_file: str = typer.Argument(None, help="Output video file"),
    decay: int = typer.Argument(None, help=""),    
    planes: str = typer.Argument(None, help="Input weight for frame delay")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file,
        "decay": decay,
        "planes": planes
    }
    defaults = config['frame_delay_pro2']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    frame_delay_pro2.frame_delay_pro2(**params)

######################
# ghostee
######################
@app.command('ghostee', help='Ghosting effect.')
def ghostee_vb(
    input_file: str = typer.Argument(None, help="Input video file"),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file, 
        "output_file": output_file
    }
    defaults = config['ghostee']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    ghostee.ghostee(**params)

######################
# light_snow
######################
@app.command('light_snow', help='Slightly smearing RGB color space.')
def light_snow_vb(
    input_file: str = typer.Argument(None, help="Input video file"),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file, 
        "output_file": output_file
    }
    defaults = config['light_snow']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    light_snow.light_snow(**params)

######################
# looper_pro
######################
@app.command('looper_pro', help='Apply video looper effect base on frame size & start frame.')
def looper_pro_vb(
    input_file: str = typer.Argument(None, help="Input video file"), 
    output_file: str = typer.Argument(None, help="Output video file"),
    loop_count: str = typer.Argument(None, help="Number of video loops"), 
    size_in_frames: str = typer.Argument(None, help="Size of loop in frames"), 
    start_frame: str = typer.Argument(None, help="Starting frame of loop")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file,
        "loop_count": loop_count,
        "size_in_frames": size_in_frames,
        "start_frame": start_frame
    }
    defaults = config['looper_pro']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    looper_pro.looper_pro(**params)

######################
# lsd_feedback
######################
@app.command('lsd_feedback', help='Apply LSD feedback effect to video file.')
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

######################
# mirror_delay
######################
@app.command('mirror_delay', help='Apply mirrored delay effect to video file.')
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

#####################
# nostalgic_stutter
#####################
@app.command('nostalgic_stutter', help='Apply nostaglic stutter effect to video file.')
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

######################
# num_edits
######################
@app.command('num_edits', help='Create a number of edits from a source file.')
def num_edits_vb(
    input_file: str = typer.Argument(None, help="Input video file "),
    output_file: str = typer.Argument(None, help="Input video file "),
    count: str = typer.Argument(None, help="Input video file ")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file,
        "count": count
    }
    defaults = config['num_edits']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    num_edits.num_edits(**params)

######################
# overexposed_stutter
######################
@app.command('overexposed_stutter', help='Apply overexposed stutter effect to video file.')
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

######################
# overlay_img_pro
######################
@app.command('overlay_img_pro', help='Overlay an image with location & dimension control.')
def overlay_img_pro_vb(
    input_file: str = typer.Argument(None, help="Input video file "),
    output_file: str = typer.Argument(None, help="Output video file"),
    overlay_image: int = typer.Argument(None, help="Image file"),    
    x_position: str = typer.Argument(None, help="X position of the image file"),    
    y_position: str = typer.Argument(None, help="Y position of the image file"),
    overlay_width: str = typer.Argument(None, help="Overlay image width"),
    overlay_height: str = typer.Argument(None, help="Overlay image height")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file,
        "overlay_image": overlay_image,
        "x_position": x_position,
        "y_position": y_position,
        "overlay_width": overlay_width,
        "overlay_height": overlay_height,
    }
    defaults = config['overlay_img_pro']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    overlay_img_pro.overlay_img_pro(**params)

######################
# pickle_juice 
######################
@app.command('pickle_juice', help='Apply filter like the video was dipped in pickle juice.')
def pickle_juice_vb(
    input_file: str = typer.Argument(None, help="Input video file"),
    output_file: str = typer.Argument(None, help="Output video file"),
):
    params = { 
        "input_file": input_file, 
        "output_file": output_file
    }
    defaults = config['pickle_juice']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    pickle_juice.pickle_juice(**params)

######################
# rb_blur 
######################
@app.command('rb_blur', help='Resize a video to the given width and height.')
def rb_blur_vb(
    input_file: str = typer.Argument(None, help="Input video file"),
    output_file: str = typer.Argument(None, help="Output video file"),
):
    params = { 
        "input_file": input_file, 
        "output_file": output_file
    }
    defaults = config['rb_blur']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    rb_blur.rb_blur(**params)

######################
# recalled_sensor
######################
@app.command('recalled_sensor', help='Applies xrgb filter')
def recalled_sensor_vb(
    input_file: str = typer.Argument(None, help='Video file you would to filter'),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['recalled_sensor']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    recalled_sensor.recalled_sensor(**params)

######################
# repainting 
######################
@app.command('repainting', help='Resize a video to the given width and height.')
def repainting_vb(
    input_file: str = typer.Argument(None, help="Input video file"),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file, 
        "output_file": output_file
    }
    defaults = config['repainting']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    repainting.repainting(**params)

######################
# resize 
######################
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

######################
# reverse
######################
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

######################
# scrolling_pro
######################
@app.command('scrolling_pro', help='Apply scrolling pro effect to video file.')
def scrolling_pro_vb(
    input_file: str = typer.Argument(None, help="Input video file"), 
    output_file: str = typer.Argument(None, help="Output video file"),    
    horizontal: str = typer.Argument(None, help="Horizontal scroll parameter"), 
    vertical: str = typer.Argument(None, help="Vertical scroll parameter")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file,
        "horizontal": horizontal,
        "vertical": vertical
    }
    defaults = config['scrolling_pro']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    scrolling_pro.scrolling_vb(**params)

######################
# septic
######################
@app.command('septic', help='Apply septic effect to video file.')
def septic_vb(
    input_file: str = typer.Argument(None, help="Input video file"), 
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['septic']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    septic.septic(**params)

######################
# silence_xtraction
######################
@app.command('silence_xtraction', help="Stitches togehter video chunks that have no discernable words." +
              "This does NOT use audio analysis, but instead identifes the presence of a 'word' using the .srt transcription file")
def silence_xtraction_vb(
    input_file: str = typer.Argument(None, help="Input video file"),
    output_file: str = typer.Argument(None, help="Output video file"),
    min_d: int = typer.Argument(None, help="Minimum duration of a chunk of silence."),
    max_d: int = typer.Argument(None, help="Maximum duration of a chunk of silence."),
    adj: int = typer.Argument(None, help="Adjustment value")
):
    params = { 
        "input_file": input_file, 
        "output_file": output_file,
        "min_d": min_d,
        "max_d": max_d,
        "adj": adj
    }

    defaults = config['silence_xtraction']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    silence_xtraction.silence_xtraction(**params)

######################
# slight_smear
######################
@app.command('slight_smear', help='Slightly smearing RGB color space.')
def slight_smear_vb(
    input_file: str = typer.Argument(None, help="Input video file"),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file, 
        "output_file": output_file
    }
    defaults = config['slight_smear']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    slight_smear.slight_smear(**params)

######################
# speed
######################
@app.command('speed', help='Apply speed effect to video file.')
def speed_vb(
    input_file: str = typer.Argument(None, help="Input video file"), 
    output_file: str = typer.Argument(None, help="Output video file"),
    speed_factor: str = typer.Argument(None, help="Playback speed")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file,
        "speed_factor": speed_factor
    }
    defaults = config['speed']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    speed.speed(**params)

######################
# smudge
######################
@app.command('smudge', help='Apply smudge effect to video file.')
def smudge_vb(
    input_file: str = typer.Argument(None, help="Input video file "),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['smudge']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    smudge.smudge(**params)

######################
# soapblind
######################
@app.command('soapblind', help='Apply soapblind effect to video file.')
def soapblind_vb(
    input_file: str = typer.Argument(None, help="Input video file "),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['soapblind']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    soapblind.soapblind(**params)

######################
# splitting
######################
@app.command('splitting', help='Apply splitting effect to video file.')
def splitting_vb(
    input_file: str = typer.Argument(None, help="Input video file"), 
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['splitting']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    splitting.splitting(**params)

######################
# stack_2x
######################
@app.command('stack_2x', help='Stack 2 videos on top of each other keeping the original orientation.')
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

######################
# steel_wash
######################
@app.command('steel_wash', help='Apply steel blue filter to video.')
def steel_wash_vb(
    input_file: str = typer.Argument(None, help="Input video file 1"),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['steel_wash']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    steel_wash.steel_wash(**params)

######################
# stutter_pro
######################
@app.command('stutter_pro', help='Apply stutter pro effect to video file.')
def stutter_pro_vb(
    input_file: str = typer.Argument(None, help="Input video file"), 
    output_file: str = typer.Argument(None, help="Output video file"),
    stutter: str = typer.Argument(None, help="Frame stutter parameter")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file,
        "stutter": stutter
    }
    defaults = config['stutter_pro']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    stutter_pro.stutter_pro(**params)

######################
# t1000
######################
@app.command('t1000', help='Applies T1000 filter')
def t1000_vb(
    input_file: str = typer.Argument(None, help='Video file you would to filter'),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['t1000']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    t1000.t1000(**params)

######################
# transcraibe
######################
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

######################
# twociz
######################
@app.command('twociz', help='Applies twociz filter')
def twociz_vb(
    input_file: str = typer.Argument(None, help='Video file you would to filter'),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['twociz']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    twociz.twociz(**params)

######################
# wbflare
######################
@app.command('wbflare', help='Applies wbflare filter')
def wbflare_vb(
    input_file: str = typer.Argument(None, help='Video file you would to filter'),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['wbflare']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    wbflare.wbflare(**params)

######################
# xrgb
######################
@app.command('xrgb', help='Applies xrgb filter')
def xrgb_vb(
    input_file: str = typer.Argument(None, help='Video file you would to filter'),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['xrgb']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    xrgb.xrgb(**params)

######################
# zapruder
######################
@app.command('zapruder', help='Apply zapruder effect to video file.')
def zapruder_vb(
    input_file: str = typer.Argument(None, help='Input video file'),
    output_file: str = typer.Argument(None, help="Output video file")
):
    params = { 
        "input_file": input_file,
        "output_file": output_file
    }
    defaults = config['zapruder']
    params = {key: params.get(key) or defaults[key] for key in defaults}
    zapruder.zapruder(**params)

if __name__ == "__main__":
    app()

