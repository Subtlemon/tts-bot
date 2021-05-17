import json
import os

from google.cloud import texttospeech


class TTSEngine:
    def __init__(self):
        path = os.path.abspath('engine/voices.json')
        print('Loading', path)
        with open(path) as file:
            self._voices = json.load(file)
        del self._voices['__source__']  # This is just a comment in the json.
        self._client = texttospeech.TextToSpeechClient()

    def text_to_speech(self, text: str, voice: str, output_file_path: str):
        synthesis_input = texttospeech.types.SynthesisInput(text=text)
        voice_spec = self._voices[voice] if voice in self._voices else self._voices['default']
        voice = texttospeech.types.VoiceSelectionParams(language_code=voice_spec['language_code'], 
                                                        name=voice_spec['name'],
                                                        ssml_gender=self._to_gender_enum(voice_spec['gender']))
        audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)
        response = self._client.synthesize_speech(input_=synthesis_input, voice=voice, audio_config=audio_config)
        
        with open(output_file_path, 'wb') as out:
            out.write(response.audio_content)

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
