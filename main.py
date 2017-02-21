from multiprocessing import Process
from os.path import exists
from stuff.api_call import *
from stuff.audio_op import *
from stuff.project import *
import argparse
import sys

def call_helper(segment, trans_filename, data):
	resp = call_single_speak(
		segment,
		username = data['username'],
		password = data['password'])
	with open(trans_filename, 'w') as t:
		t.write(resp.text)
		print("Transcribed:\t", trans_filename)

if len(sys.argv) < 2:
	print("ERROR: No video file supplied.")
	print("Syntax: python main.py <video_file>")
	sys.exit(2)

video_file = sys.argv[1]

# Create a project using the video file supplied in the original call
p = Project(video_file)
p.create_req_paths()
p.get_credentials()

# Extract and segment the audio from the video. Then, construct a list of segments
audio_extraction(video_file, p.audio_dest)
audio_segmentation(p.audio_dest, p.audio_seg_path)
p.segment_names()

jobs = []

for seg in p.seg_list:
	time_filename = splitext(basename(seg))[0]
	trans_filename = join(p.trans_path, time_filename) + ".json"
	if not exists(trans_filename):
		print("Sending to Watson Speech-to-Text:\n\t", trans_filename)
		job = Process(target=call_helper,args=(seg, trans_filename, p.data))
		job.start()
		jobs.append(job)

for job in jobs:
	job.join()