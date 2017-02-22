from multiprocessing import Process
from os.path import exists
from stuff.api_call import *
from stuff.audio_op import *
from stuff.project import *
import argparse
import json
import sys

def call_helper(segment, trans_filename, data):
	resp = call_single_speak(
		segment,
		username = data['username'],
		password = data['password'])
	with open(trans_filename, 'w') as t:
		t.write(resp.text)
		print("Transcribed:\n\t", trans_filename)

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

jobs = []	# list of jobs for multithreading purposes

# For each segment, create a process that will handle the api call for
# that part and write the response to a JSON file of the same name
for seg in p.seg_list:
	time_filename = splitext(basename(seg))[0]
	trans_filename = join(p.trans_path, time_filename) + ".json"
	if not exists(trans_filename):
		print("Sending to Watson Speech-to-Text:\n\t", time_filename)
		job = Process(target=call_helper,args=(seg, trans_filename, p.data))
		job.start()
		jobs.append(job)

for job in jobs:
	job.join()

# Generate a sorted list of transcript JSON files
p.transcript_names()

# For each transcript JSON, print the transcripts of highest confidence
for trans in p.trans_list:
	with open(trans) as data_file:
		data = json.load(data_file)
	for result in data["results"]:
		print(result["alternatives"][0]["transcript"])
		print("\n")