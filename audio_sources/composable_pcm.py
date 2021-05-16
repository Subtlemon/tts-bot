import audioop

from discord import AudioSource
from threading import Lock


class ComposablePCM(AudioSource):
    def __init__(self, initial_source):
        self._sources = [initial_source]
        self._lock = Lock()

    def read(self):
        """Overridden."""
        self._lock.acquire()
        bytes = self._read_unsafe()
        self._lock.release()
        if not bytes:
            return b''
        else:
            return bytes

    def add_source(self, new_source) -> bool:
        """Returns false if the current source is ended and a new source should be made."""
        sources_valid = False
        self._lock.acquire()
        if self._sources:
            self._sources.append(new_source)
            sources_valid = True
        self._lock.release()
        return sources_valid

    def _read_unsafe(self) -> bytes:
        """Read audio from sources in an un-thread-safe manner."""
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
        return bytes
