import os
import urllib.parse
import urllib.request

from dotenv import load_dotenv


load_dotenv()
TTS_SPECIAL_CLIENT_URL = os.getenv('TTS_SPECIAL_CLIENT_URL')


class TTSSpecialClient:
    def tts(self, text, name):
        """Performs a TTS request in the form of 'TTS_SPECIAL_CLIENT_URL?text=<text>&name=<name>'."""
        params = {'text': urllib.parse.quote(text), 'name': name}
        # Create request url.
        url_parse = urllib.parse.urlparse(TTS_SPECIAL_CLIENT_URL)
        query = url_parse.query
        url_dict = dict(urllib.parse.parse_qsl(query))
        url_dict.update(params)
        url_new_query = urllib.parse.urlencode(url_dict)
        url_parse = url_parse._replace(query=url_new_query)
        request_url = urllib.parse.urlunparse(url_parse)
        # Make request and return content.
        return urllib.request.urlopen(request_url).read()

    def is_enabled(self):
        return TTS_SPECIAL_CLIENT_URL is not None
