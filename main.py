# Author: Alexander Decurnou
# Team: iDev

from multiprocessing import Process
from os import path
from stuff import api_call
from stuff import audio_op
from stuff import project
from stuff import srt_maker
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("file", help="the video (or audio-only) file to be transcribed")
parser.add_argument("-a", "--audio_only", help="use when there is only audio (no video) supplied", action="store_true")
parser.add_argument("-m", "--multi", help="turn on multi-speaker detection", action="store_true")
parser.add_argument("-ns", "--no_seg", help="process audio in one file, instead of segments", action="store_true")
parser.add_argument("-ga", "--give_alts", help="give alternative transcripts as well", action="store_true")
parser.add_argument("-sl", "--seg_length", help="length of segments in seconds", type=int)

args = parser.parse_args()


def call_helper(audio, trans_filename, data, flag_multi):
    if flag_multi:
        resp = api_call.call_multi_speak(
            audio,
            username=data['username'],  # If multi-speaker detection is
            password=data['password'])  # requested, run call_multi_speak.
    else:
        resp = api_call.call_single_speak(
            audio,
            username=data['username'],  # Otherwise, run the method for
            password=data['password'])  # single speakers
    with open(trans_filename, 'w') as t:
            t.write(resp.text)
            print("Transcribed:\n\t", trans_filename)


# Create a project using the video file supplied in the original call
p = project.Project(args.file, args.no_seg, args.multi, args.audio_only, args.give_alts)

p.create_req_paths()
p.get_credentials()

# Segment the audio from the video, then construct a list of segments
if not p.flag_audio_only:
    audio_op.audio_extraction(p.filename, p.audio_dest)
else:
    audio_op.audio_conversion(p.filename, p.audio_dest)

if not p.flag_no_seg:
    audio_op.audio_segmentation(p.audio_dest, p.audio_seg_path)
    p.segment_names()

    jobs = []   # list of jobs for multithreading purposes

    # For each segment, create a process that will handle the api call for
    # that part and write the response to a JSON file of the same name
    for seg in p.seg_list:
        time_filename = path.splitext(path.basename(seg))[0]
        trans_filename = path.join(p.trans_path, time_filename) + ".json"
        if not path.exists(trans_filename):
            print("Sending to Watson Speech-to-Text:\n\t", time_filename)
            job = Process(target=call_helper, args=(seg, trans_filename, p.data, p.flag_multi))
            job.start()
            jobs.append(job)

    for job in jobs:
        job.join()
else:
    trans_filename = path.join(p.trans_path, p.slug) + ".json"
    if not path.exists(trans_filename):
        print("Sending audio to Watson Speech-to-Text.")
        call_helper(p.audio_dest, trans_filename, p.data, p.flag_multi)

# Generate a sorted list of transcript JSON files
p.transcript_names()

# For each transcript JSON, write both the transcripts of highest confidence
# and any alternative transcripts that may have been supplied to a file
"""with open(p.full_transcript_path, 'w') as f:
    for trans in p.trans_list:
        with open(trans) as data_file:
            data = json.load(data_file)
        for result in data["results"]:
            timestamps = result["alternatives"]["timestamps"]
            best = alts.pop(0)
            if not p.flag_give_alts:
                f.write(best["transcript"] + "\n")
            else:
                f.write("Best Confidence Transcript:\n")
                f.write(best["transcript"] + "\n")
                f.write("Alternative Transcripts:\n")
                for item in alts:
                    f.write(item["transcript"] + "\n")
                f.write("\n")"""

s = srt_maker.SRT(trans_filename, p.slug)
s.write_to_file(p.path)