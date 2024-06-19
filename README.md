#  videobeaux

## Description
Your friendly multilateral video toolkit built for artists by artists. It's your best friend.

## Available Programs
| Program | Description |
| -------- | ------- | 
| convert | Simple video file convert | 
| extract_frames | Extract individuals frames from a video file as PNGs | 
| resize | Resizing the dimensions of a video file | 
| silence_extraction | Extracting the silence out of a video file | 

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








