from multiprocessing import Process
from os.path import exists
from stuff.api_call import *
from stuff.audio_op import *
from stuff.project import *
import argparse
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument("file", help="the video (or audio-only) file to be transcribed")
parser.add_argument("-a", "--audio_only", help="use when there is only audio (no video) supplied", action="store_true")
parser.add_argument("-m", "--multi", help="turn on multi-speaker detection", action="store_true")
parser.add_argument("-ns", "--no_seg", help="process audio in one file, instead of segments", action="store_true")
args = parser.parse_args()

# If multi-speaker detection is requested, run call_multi_speak. Otherwise, run the method for single speakers.
def call_helper(audio, trans_filename, data, flag_multi):
	if flag_multi:
		resp = call_multi_speak(
			audio,
			username = data['username'],
			password = data['password'])
	else:
		resp = call_single_speak(
			audio,
			username = data['username'],
			password = data['password'])	
	with open(trans_filename, 'w') as t:
			t.write(resp.text)
			print("Transcribed:\n\t", trans_filename)

# Create a project using the video file supplied in the original call
p = Project(args.file, args.no_seg, args.multi, args.audio_only)
p.create_req_paths()
p.get_credentials()

# Extract and segment the audio from the video. Then, construct a list of segments
if not p.flag_audio_only:
	audio_extraction(p.filename, p.audio_dest)
else:
	audio_conversion(p.filename, p.audio_dest)

if not p.flag_no_seg:
	audio_segmentation(p.audio_dest, p.audio_seg_path)
	p.segment_names()

	jobs = []	# list of jobs for multithreading purposes

	# For each segment, create a process that will handle the api call for
	# that part and write the response to a JSON file of the same name
	for seg in p.seg_list:
		time_filename = splitext(basename(seg))[0]
		trans_filename = join(p.trans_path, time_filename) + ".json"
		if not exists(trans_filename):
			print("Sending to Watson Speech-to-Text:\n\t", time_filename)
			job = Process(target=call_helper,args=(seg, trans_filename, p.data, p.flag_multi))
			job.start()
			jobs.append(job)

	for job in jobs:
		job.join()
else:
	trans_filename = join(p.trans_path, p.slug) + ".json"
	if not exists(trans_filename):
		call_helper(p.audio_dest, trans_filename, p.data, p.flag_multi)

# Generate a sorted list of transcript JSON files
p.transcript_names()

# For each transcript JSON, write both the transcripts of highest confidence
# and any alternative transcripts that may have been supplied to a file
with open(p.full_transcript_path, 'w') as f:
	for trans in p.trans_list:
		with open(trans) as data_file:
			data = json.load(data_file)
		for result in data["results"]:
			alts = result["alternatives"]
			best = alts.pop(0)
			f.write("Best Confidence Transcript:\n")
			f.write(best["transcript"] + "\n")
			f.write("Alternative Transcripts:\n")
			for item in alts:
				f.write(item["transcript"] + "\n")
			f.write("\n")