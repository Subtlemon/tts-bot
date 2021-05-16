import audioop

from discord import AudioSource


class ComposablePCM(AudioSource):
    def __init__(self, initial_source):
        self._sources = [initial_source]

    def read(self):
        bytes = None
        playing_sources = []
        for source in self._sources:
            curr_bytes = source.read()
            if not curr_bytes:
                source.cleanup()
                continue
            else:
                playing_sources.append(source)
            if not bytes:
                bytes = curr_bytes
            else:
                bytes = audioop.add(bytes, curr_bytes, 2)
        self._sources = playing_sources
        if not bytes:
            return b''
        else:
            return bytes

    def add_source(self, new_source):
        self._sources.append(new_source)