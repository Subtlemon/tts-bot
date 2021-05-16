import os

from discord import AudioSource


class ResourceOwningSource(AudioSource):
    def __init__(self, source, owned_file_path):
        self._source = source
        self._owned_file_path = owned_file_path

    def is_opus(self):
        return self._source.is_opus()

    def read(self):
        """Overridden."""
        return self._source.read()

    def cleanup(self):
        """Overridden."""
        self._source.cleanup()
        if os.path.exists(self._owned_file_path):
            os.remove(os.path.abspath(self._owned_file_path))
