from glob import glob
from os import makedirs
from os.path import join, basename, splitext, expanduser, abspath
import json

PROJECTS_DIR = join(".", "projects")
WATSON_CREDENTIALS = "watson_creds.json"
FULL_TRANSCRIPT_BASENAME = 'full-transcript.json'
LINES_TRANSCRIPT_BASENAME = 'lines-transcript.csv'
WORDS_TRANSCRIPT_BASENAME = 'words-transcript.csv'

class Project:
	# Set the project slug to the filename of the video
	def __init__(self, filename):
		self.slug = splitext(basename(filename))[0]
		self.audio_dest = self.slug + ".wav"

	def make_proj_dir(self):
		"""
		This will take the project's slug and expand to the full path. It will
		then attempt to create a directory for the project. exist_ok is set to
		True as it will not wipe the directory if it already exists, which is 
		fine in my case
		""" 
		xslug = self.slug.replace("projects/", "").rstrip('/')
		try:
			self.path = join(PROJECTS_DIR, xslug)
			self.path = abspath(expanduser(self.path))
			makedirs(self.path, exist_ok = True)
			print("Project directory " + self.slug + " created.")
		except OSError as ex:
			if ex.errno != errno.EEXIST:
				print("Project directory cannot be created!")
				raise

	# Same as make_proj_dir, only it creates a subfolder in the project folder
	def audio_seg_dir(self):
		try:
			self.audio_seg_path = join(self.path, "audio_seg")
			makedirs(self.audio_seg_path, exist_ok = True)
			print("Audio segement directory for project created.")
		except OSError as ex:
			if ex.errno != errno.EEXIST:
				print("Audio segment directory cannot be created!")
				raise

	# Seems to be a pattern here.
	def transcripts_dir(self):
		try:
			self.trans_path = join(self.path, "transcripts")
			makedirs(self.trans_path, exist_ok = True)
			print("Transcript directory for project created")
			self.full_transcript_path = join(self.path, FULL_TRANSCRIPT_BASENAME)
			self.lines_transcript_path = join(self.path, LINES_TRANSCRIPT_BASENAME)
			self.words_transcript_path = join(self.path, WORDS_TRANSCRIPT_BASENAME)
		except OSError as ex:
			if ex.errno != errno.EEXIST:
				print("Transcript directory cannot be created!")
				raise

	# Easy way to create the required folders
	def create_req_paths(self):
		self.make_proj_dir()
		self.audio_seg_dir()
		self.transcripts_dir()

	# This will create a list of each of the audio segments found in a project.
	def segment_names(self):
		self.seg_list = glob(join(self.audio_seg_path, '*.wav'))

	# This will create a list of each of the transcripts in a project folder
	def transcript_names(self):
		self.trans_list = glob(join(self.trans_path, '*.json'))
		self.trans_list = sorted(self.trans_list, key=lambda x: int(basename(x).split('-')[0]))

	# This will load the credentials for the Bluemix service
	def get_credentials(self, filename=WATSON_CREDENTIALS):
		with open(filename, 'r') as f:
			self.data = json.load(f)