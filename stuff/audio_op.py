# Author: Alexander Decurnou
# Team: iDev

from math import ceil
from moviepy.editor import VideoFileClip, AudioFileClip
from os.path import join
import subprocess

DEFAULT_AUDIOFILE_CODEC = 'libvorbis'  # used to create webms
DEFAULT_AUDIOFILE_BITRATE = None
DEFAULT_ZEROES_PADDING = 5
DEFAULT_AUDIO_SEGMENT_DURATION_SEC = 180


def audio_extraction(path, audio_dest, audio_codec=DEFAULT_AUDIOFILE_CODEC,
                     audio_bitrate=DEFAULT_AUDIOFILE_BITRATE):
    try:
        print("Extracting audio...")
        #video = VideoFileClip(vid_src)
        #audio = video.audio
        #audio.write_audiofile(audio_dest, codec=audio_codec,
        #                      bitrate=audio_bitrate, verbose=False,
        #                      progress_bar=False)
        command = "ffmpeg -i {} -vn -acodec {} -y {}".format(path, audio_codec, audio_dest)
        subprocess.call(command, shell=True)
        print("Audio file extracted.")
    except:
        print("Unexpected error!")
        raise


# Really hacky way of making audio-only files into audio-only webms. Yes,
# transcoding from lossy to lossy is bad, but since this will be used on mostly
# voice-only stuff, I'm not terribly worried about a loss of fidelity.
def audio_conversion(audio_src, audio_dest, audio_codec=DEFAULT_AUDIOFILE_CODEC,
                     audio_bitrate=DEFAULT_AUDIOFILE_BITRATE):
    try:
        print("Extracting audio...")
        audio = AudioFileClip(audio_src)
        audio.write_audiofile(audio_dest, codec=audio_codec,
                              bitrate=audio_bitrate, verbose=False,
                              progress_bar=False)
        print("Audio file extracted.")
    except:
        print("Unexpected error!")
        raise


def audio_segmentation(audio_src, audio_seg_dir,
                       seg_dur=DEFAULT_AUDIO_SEGMENT_DURATION_SEC,
                       pad_zeroes=DEFAULT_ZEROES_PADDING):
    src_ext = ".webm"
    audio = AudioFileClip(audio_src)
    total_sec = audio.duration
    start_sec = 0

    print("Segmenting audio...")
    while start_sec < total_sec:
        end_sec = start_sec + seg_dur
        if end_sec > total_sec:
            end_sec = ceil(total_sec)
            segment = audio.subclip(start_sec)
        else:
            segment = audio.subclip(start_sec, end_sec)
        seg_name = "%s-%s%s" % (
            str(start_sec).rjust(pad_zeroes, "0"),
            str(end_sec).rjust(pad_zeroes, "0"), src_ext)
        start_sec = end_sec
        seg_full_path = join(audio_seg_dir, seg_name)
        segment.write_audiofile(seg_full_path, codec=DEFAULT_AUDIOFILE_CODEC,
                                bitrate=DEFAULT_AUDIOFILE_BITRATE,
                                verbose=False, progress_bar=False)

    print("Audio segmentation complete.")
