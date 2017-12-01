# Author: Alexander Decurnou
# Team: iDev

from glob import glob
from os import makedirs
from os.path import join, basename, splitext, expanduser, abspath
import json
import math

class SRT(object):
	"""
	This will take the TXT file generated from the API call and turn
	it into an SRT file with timestamps.
	"""
	def __init__(self, text, slug):
		self.text = text
		self.filename = slug + '.srt'

	pieces = []
	time_ranges = []

	def _collect_pieces(self):
		with open(self.text, 'r') as f:
			j = json.loads(f.read())
			print("Transcript successfully read.")
			n = len(j['results'])
			print("{} chunks in transcript".format(n))
			for i in range(n-1):
				print(i)
				self.pieces.append(j['results'][i]['alternatives'][0]['transcript'])
				self.time_ranges.append((j['results'][i]['alternatives'][0]['timestamps'][0][1], 
					                     j['results'][i]['alternatives'][0]['timestamps'][-1][2]))
			return(list(zip(self.pieces, self.time_ranges)))

	def _time_conversion(self, time_seconds):
		s = time_seconds
		m, s = divmod(s, 60)
		h, m = divmod(m, 60)
		return(("%d:%02d:%02d,000" % (h, m, s)))

	def _create_file(self):
		pieces = self._collect_pieces()
		num_chunks = len(pieces)
		temp_chunk = []
		for i in range(num_chunks):
			temp_chunk.append(str(i+1) + "\n")                    # line one

			begin = self._time_conversion(pieces[i][1][0])
			end = self._time_conversion(pieces[i][1][1])
			temp_chunk.append("{} --> {} \n".format(begin, end))  # line two

			temp_chunk.append(str(pieces[i][0]) + "\n")           # line three
			temp_chunk.append("\n")                               # line four

		return temp_chunk

	def write_to_file(self, path):
		captions = self._create_file()
		with open(join(path, self.filename), 'w') as f:
			f.writelines(captions)
