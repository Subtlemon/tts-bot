import os
import pickledb


class LocalStore:
    def __init__(self, file_path):
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        self._db = pickledb.load(file_path, auto_dump=True)

    def get_voice(self, guild_id: int, user_id: int) -> str:
        key = f'{guild_id}:{user_id}:voice'
        return self._db.get(key)

    def set_voice(self, guild_id: int, user_id: int, voice: str) -> int:
        key = f'{guild_id}:{user_id}:voice'
        self._db.set(key, voice)
