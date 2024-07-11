<p align="center">
  <img width="45%" height="45%" src="https://github.com/vondas-network/videobeaux/blob/main/img/videobeaux-1.png?raw=true"/>  
</p>

<p align="center"><em>Your friendly multilateral video toolkit built for artists by artists. It's your best friend.</em></p> 

## Available Programs
| Program | Description |
| -------- | ------- | 
| bad_contrast | Apply a bad constrast effect | 
| blur_pix | Extracting the silence out of a video file | 
| bpred | Apply bad Predator heat vision effect | 
| convert | Simple video file convert | 
| double_cup | Apply the effect of purple drank | 
| download_yt | Video ripper | 
| extract_frames | Extract individuals frames from a video file as PNGs | 
| extract_sound | Extract audio from video file |
| frame_delay_pro1 | Apply frame delay effect with parameter input | 
| frame_delay_pro2 | Apply frame delay effect with parameter input | 
| looper_pro | Apply video looper effect base on frame size & start frame | 
| lsd_feedback | Apply LSD-like frame delay effect | 
| mirror_delay | Apply a frame delay plus a mirrored effect | 
| nostalgic_stutter | Apply frame stutter akin to a corrupted file | 
| overexposed_stutter | Apply a frame stutter and exposing the video like the file is corrupted | 
| overlay_img_pro | Overlay an image with location & dimension control | 
| resize | Resizing the dimensions of a video file |
| reverse | Reverse video file | 
| scrolling_pro | Apply video scrolling effect with definable parameters | 
| scrolling | Apply static video scrolling effect | 
| silence_extraction | Extracting the silence out of a video file |  
| slight_smear | Slightly smearing RGB color space |  
| speed | Change the video and audio speed of a file |  
| stack_2x | Stack 2 videos on top of each other keeping the original orientation | 
| stutter_pro | Apply frame stutter effect with definable parameters | 
| transraibe | AI-based transcription tool | 

## Dependencies
FFmpeg is required for the project. Install *ffmpeg* using [Homebrew](https://formulae.brew.sh/formula/ffmpeg)
```bash
brew install ffmpeg
```

## Requirements

Install the project requirements
``` bash
pip install -r requirements.txt
```

## Project setup

### Create Python virtual environment
In a nutshell, Python virtual environments help decouple and isolate Python installs and associated pip packages. This allows end-users to install and manage their own set of packages that are independent of those provided by the system or used by other projects.
```bash
 cd videobeaux
 python -m venv env
```

### Activate Virtual Environment
This will activate your virtual environment. Immediately, you will notice that your terminal path includes env, signifying an activated virtual environment.

``` bash
source env/bin/activate
```

## Examples

### Using the config file
Use the *config* file to define the parameters of the function. It acts as a template for the program you'd like to run.

Define parameters in the *config* file 
``` text
resize:
  input_file: "input_file.mp4"
  output_file: "output_resized_again.mp4"
  width: 1200
  height: 200
```
  
Run the program.
``` bash
videobeaux.py resize-video
```

### Inline Commands  
Define the parameters of the command using inline parameters.

``` bash
python videobeaux.py resize-video --input_video input_file.mp4 --output_video resized.mp4 --height 400 --width 300
```

## Help
Learn more about a program using the *help* command

### Usage

```
python videobeaux.py convert-video --help 
```

### Response

```  bash
Usage: videobeaux.py convert-video [OPTIONS]

  Convert a video to a different format.

Options:
  --input-file TEXT   Input video file
  --output-file TEXT  Output video file
  --format TEXT       Format of the output video
  --help              Show this message and exit.
```

## Video Exaxmples

bad_contrast

https://github.com/vondas-network/videobeaux/assets/7625379/9ba59b08-79a8-4a09-8b18-c0fe90a6c5e2

blur_pix

https://github.com/vondas-network/videobeaux/assets/7625379/65403294-3e34-4ff8-816a-5de7c80c811d

broken_scroll

https://github.com/vondas-network/videobeaux/assets/7625379/4cdebccc-8519-45c6-aded-089db73d20d2

double_cup

https://github.com/vondas-network/videobeaux/assets/7625379/83d30a18-40d1-42e4-aff3-dbd50d67a7d1

frame_delay_pro1-1

https://github.com/vondas-network/videobeaux/assets/7625379/871ccdb9-ae2b-46e1-8b0f-0514eb92e1aa

frame_delay_pro1-2

https://github.com/vondas-network/videobeaux/assets/7625379/0a727474-25cf-42ab-a717-583e12b4a04d

frame_delay_pro1-3

https://github.com/vondas-network/videobeaux/assets/7625379/5ab60f24-b4e2-4e0e-abc0-cfab62e09cda

frame_delay_pro2-1

https://github.com/vondas-network/videobeaux/assets/7625379/a88284bc-ca7e-4355-8f95-377434c61d13

frame_delay_pro2-2

https://github.com/vondas-network/videobeaux/assets/7625379/acf571e7-7162-413f-80f8-769815093267

frame_delay_pro2-3

https://github.com/vondas-network/videobeaux/assets/7625379/f717d419-687b-4cc3-ac07-64f45c763531

lsd_feedback

https://github.com/vondas-network/videobeaux/assets/7625379/9653929c-30ad-4c72-81c8-e3777c590783

looper_pro

https://github.com/vondas-network/videobeaux/assets/7625379/01090d49-8626-4fc0-b55c-807d100a78fa

mirror_delay

https://github.com/vondas-network/videobeaux/assets/7625379/a3dea5c6-03a6-4f65-951d-211f50457b63

nostalgic

https://github.com/vondas-network/videobeaux/assets/7625379/3cef37d9-093f-4bd9-850c-4b163e8a3e01

overexposed_stutter

https://github.com/vondas-network/videobeaux/assets/7625379/f7250a1e-3cf5-4826-977a-a5a18b231ddb

overlay_img_pro

https://github.com/vondas-network/videobeaux/assets/7625379/3932d910-b898-4ed7-ba3a-288a708c0d83

reverse

https://github.com/vondas-network/videobeaux/assets/7625379/74367227-6fee-455f-af36-804a1e6d6cb6

scrolling_pro-1

https://github.com/vondas-network/videobeaux/assets/7625379/e84cfb49-f72d-449e-833a-0271903704f4

scrolling_pro-2

https://github.com/vondas-network/videobeaux/assets/7625379/19c6eef1-2bc0-4d84-b531-55f9ca07a912

scrolling_pro-3

https://github.com/vondas-network/videobeaux/assets/7625379/4a4272de-e074-4e37-8c2d-a282f2d8be57

speed

https://github.com/vondas-network/videobeaux/assets/7625379/c27efdb1-ae81-4d8d-a153-de6294b7fedf

stack_2x

https://github.com/vondas-network/videobeaux/assets/7625379/6f244aba-e741-46c9-9863-7fc43527a8d6

stutter_pro-1

https://github.com/vondas-network/videobeaux/assets/7625379/03e234fb-d0fe-4d72-a11c-dff1bc59fa83

stutter_pro-2

https://github.com/vondas-network/videobeaux/assets/7625379/e6d8c14a-9f20-4365-bb1f-5f473289a855

stutter_pro-3

https://github.com/vondas-network/videobeaux/assets/7625379/864835ba-dc9d-4392-aa77-2cc062e2b700
