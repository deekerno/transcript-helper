import requests

ENDPOINT = 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize'

HEADERS = {
    'content-type': 'audio/webm'
}

PARAMS_SINGLE = {
    'continuous': True,
    'max_alternatives': 3,
    'profanity_filter': False,
    'smart_formatting': True,
    'timestamps': True,
    'word_alternatives_threshold': 0.35,
    'word_confidence': True
}

PARAMS_MULTI = {
    'continuous': True,
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
            auth=(username, password),
            data=f,
            params=PARAMS_SINGLE,
            headers=HEADERS,
            stream=False)
        return response


def call_multi_speak(audio_file, username, password):
    with open(audio_file, 'rb') as f:
        response = requests.post(
            ENDPOINT,
            auth=(username, password),
            data=f,
            params=PARAMS_MULTI,
            headers=HEADERS,
            stream=False)
        return response
