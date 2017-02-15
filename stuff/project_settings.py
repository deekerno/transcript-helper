from glob import glob
from os import makedirs
from os.path import join, basename, splitext, expanduser, abspath, isdir
import json

PROJECTS_DIR = join(".", "projects")
WATSON_CREDENTIALS = "watson_creds.json"
FULL_TRANSCRIPT_BASENAME = 'full-transcript.json'
LINES_TRANSCRIPT_BASENAME = 'lines-transcript.csv'
WORDS_TRANSCRIPT_BASENAME = 'words-transcript.csv'

class Project:
	def __init__(self, path_to_vid):
		self.slug = splitext(basename(path_to_vid))[0]

	def make_proj_dir():
		xslug = self.slug.replace("projects/", "").rstrip('/')
		try:
			self.path = join(PROJECTS_DIR, xslug)
			self.path = abspath(expanduser(self.path))
			makedirs(self.path, exist_ok = True)
			print("Project directory " + self.slug + "created.")
		except OSError as ex:
			if ex.errno != errno.EEXIST:
				print("Project directory cannot be created!")
				raise

	def audio_seg_dir():
		make_proj_dir()
		try:
			self.audio_seg_path = join(self.path, "audio_seg")
			makedirs(self.audio_seg_path, exist_ok = True)
			print("Audio segement directory for project created.")
		except OSError as ex:
			if ex.errno != errno.EEXIST:
				print("Audio segment directory cannot be created!")
				raise

	def transcripts_dir():
		make_proj_dir()
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

	def create_req_paths():
		audio_seg_dir()
		transcripts()

	def transcript_names():
		self.trans_list = glob(join(self.trans_path, '*.json'))

		

def get_credentials(filename=WATSON_CREDENTIALS):
	fullname = abspath(expanduser(filename))
	with open(fullname, 'r') as f:
		data = json.load(f)
		return data['creds']