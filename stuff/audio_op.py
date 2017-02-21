from math import ceil
from moviepy.editor import VideoFileClip, AudioFileClip
from os.path import splitext, join

DEFAULT_VIDEO_AUDIO_CODEC = 'libmp3lame'
DEFAULT_AUDIOFILE_CODEC = 'pcm_s16le' # 16-bit WAV
DEFAULT_AUDIOFILE_BITRATE = '16k'
DEFAULT_ZEROES_PADDING = 5
DEFAULT_AUDIO_SEGMENT_DURATION_SEC = 60

def audio_extraction(vid_src, audio_dest, audio_codec=DEFAULT_AUDIOFILE_CODEC,
				audio_bitrate=DEFAULT_AUDIOFILE_BITRATE):
	try:
		video = VideoFileClip(vid_src)
		audio = video.audio
		audio.write_audiofile(audio_dest, codec=audio_codec, bitrate=audio_bitrate)
		print("Audio file extracted.")
	except:
		print("Unexpected error!")
		raise

def audio_segmentation(audio_src, audio_seg_dir,
					seg_dur=DEFAULT_AUDIO_SEGMENT_DURATION_SEC,
					pad_zeroes=DEFAULT_ZEROES_PADDING):
	src_basename, src_ext = splitext(audio_src)
	audio = AudioFileClip(audio_src)
	total_sec = audio.duration
	start_sec = 0

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
		segment.write_audiofile(seg_full_path)

	print("Audio segmentation complete.")
