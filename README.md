# transcript-helper
A utility that uses IBM's Bluemix Speech-to-Text service to assist in adding transcripts to videos in order to maintain ADA compliance at a particular institution of higher learning. Basically, it makes my job easier. Heavily influenced by Dan Nguyen's [watson-word-watcher](https://github.com/dannguyen/watson-word-watcher).

## Getting Started
### Requirements
You will need the following packages, which can easily be installed using your favorite Python package manager. The exception to this is ffmpeg, which can just as easily be installed to your system.
```
ffmpeg
moviepy
requests
youtube-dl
```

You will also need an account with IBM's Bluemix service. After creating an account, generate credentials for the Speech-to-Text service and save them in a file called `watson_creds.json`. which is to be placed in the root directory of the repository.

### Modifications
You may want to change a few of the default options in the `audio_op.py` module found in the stuff folder. Please refer to the Bluemix API documentation for more information.

## Usage
1. Download the video to be transcribed using youtube-dl.
  * Right now, the code takes the video as an MP4. Feel free to change it or use the following snippet to download the video in the correct format: `youtube-dl -f mp4 -o *output_file.mp4* *full_YouTube_url*`
2. Run python main.py *video_file*

And that's it! The utility will create all the folders needed to organize the intermediary data. It will extract and segment the audio according to the defined parameters, and then (using multiple threads) send the segments to the Bluemix API for transcription. The transcripts will be compiled in the transcripts folder of the respective project directory.