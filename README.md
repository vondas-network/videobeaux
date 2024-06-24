#  videobeaux

## Description
Your friendly multilateral video toolkit built for artists by artists. It's your best friend.

## Available Programs
| Program | Description |
| -------- | ------- | 
| blur_pix | Extracting the silence out of a video file | 
| convert | Simple video file convert | 
| extract_frames | Extract individuals frames from a video file as PNGs | 
| frame_delay_pro1 | Apply frame delay effect with parameter input | 
| frame_delay_pro2 | Apply frame delay effect with parameter input | 
| lsd_feedback | Apply LSD-like frame delay effect | 
| mirror_delay | Apply a frame delay plus a mirrored effect | 
| nostalgic_stutter | Apply frame stutter akin to a corrupted file | 
| overexposed_stutter | Apply a frame stutter and exposing the video like the file is corrupted | 
| resize | Resizing the dimensions of a video file |
| reverse | Reverse video file | 
| scrolling_pro | Apply video scrolling effect with definable parameters | 
| scrolling | Apply static video scrolling effect | 
| silence_extraction | Extracting the silence out of a video file | 
| sound | Extract audio from video file | 
| stack_2x | Stack 2 videos on top of each other keeping the original orientation | 
| stutter_pro | Apply frame stutter effect with definable parameters | 

## Dependencies
FFmpeg is required for the project. Install *ffmpeg* using [Homebrew](https://formulae.brew.sh/formula/ffmpeg)
```bash
brew install ffmpeg
```

## Installation
Install the project requirements
``` bash
pip install -r requirements.txt
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






