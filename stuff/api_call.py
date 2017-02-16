import requests

ENDPOINT = 'https://stream.watsonplatform.net/speech-to-text/api'

HEADERS = {
	'content-type': 'audio/wav'
}

PARAMS_SINGLE = {
	'continous': True,
	'max_alternatives': 3,
	'profanity_filter': False,
	'smart_formatting': True,
	'timestamps': True,
	'word_alternatives_threshold': 0.35,
	'word_confidence': True
}

PARAMS_MULTI = {
	'continous': True,
	'max_alternatives': 3,
	'profanity_filter': False,
	'smart_formatting': True,
	'speaker_labels': True,
	'timestamps': True,
	'word_alternatives_threshold': 0.35,
	'word_confidence': True
}

def call_single_speak(audio_file, username, password):
	with open(audio_file, 'rb') as f:
		response = requests.post(
			ENDPOINT,
			auth = (username, password),
			data = f,
			params = PARAMS_SINGLE,
			headers = HEADERS,
			stream = false)
		return response

def call_multi_speak(audio_file, username, password):
	with open(audio_file, 'rb') as f:
		response = requests.post(
			ENDPOINT,
			auth = (username, password),
			data = f,
			params = PARAMS_MULTI,
			headers = HEADERS,
			stream = false)
		return response