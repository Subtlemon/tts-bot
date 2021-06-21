import json
import os

from engine.tts_special_client import TTSSpecialClient
from google.cloud import texttospeech


class TTSEngine:
    def __init__(self):
        path = os.path.abspath('engine/voices.json')
        print('Loading', path)
        with open(path) as file:
            self._voices = json.load(file)
        del self._voices['__source__']  # This is just a comment in the json.
        self._client = texttospeech.TextToSpeechClient()
        self._special_client = TTSSpecialClient()

        # Remove special voices if special voices are not enabled.
        if not self._special_client.is_enabled():
            self._voices = {voice: spec for voice, spec in self._voices.items() if 'special' not in spec}

    def text_to_speech(self, text: str, voice: str, output_file_path: str):
        voice_spec = self._voices[voice] if voice in self._voices else self._voices['default']

        is_special = 'special' in voice_spec
        if not self._special_client.is_enabled() and is_special:
            print('Warning: special voice requested, but special voices are not enabled. Using default voice instead.')
            voice_spec = self._voices['default']
            is_special = False

        if is_special:
            response_audio = self._special_client.tts(text, name=voice)
        else:
            synthesis_input = texttospeech.types.SynthesisInput(text=text)
            voice = texttospeech.types.VoiceSelectionParams(language_code=voice_spec['language_code'], 
                                                            name=voice_spec['name'],
                                                            ssml_gender=self._to_gender_enum(voice_spec['gender']))
            audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)
            response = self._client.synthesize_speech(input_=synthesis_input, voice=voice, audio_config=audio_config)
            response_audio = response.audio_content
        
        with open(output_file_path, 'wb') as out:
            out.write(response_audio)

    def all_voices(self):
        return self._voices.keys()

    def is_voice_valid(self, voice: str):
        return voice in self._voices

    def _to_gender_enum(self, gender: str):
        if gender == 'MALE':
            return texttospeech.enums.SsmlVoiceGender.MALE
        elif gender == 'FEMALE':
            return texttospeech.enums.SsmlVoiceGender.FEMALE
        else:
            return texttospeech.enums.SsmlVoiceGender.NEUTRAL
