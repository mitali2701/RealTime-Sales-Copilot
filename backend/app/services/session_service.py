import json
import os

import redis


class SessionService:
    _memory_store: dict[str, list[str]] = {}

    def __init__(self):
        self.client = redis.Redis.from_url(
            os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            decode_responses=True,
            socket_connect_timeout=0.1,
        )
        self.redis_available = False

        try:
            self.client.ping()
            self.redis_available = True
        except (redis.RedisError, OSError):
            self.redis_available = False

    def _key(self, session_id: str) -> str:
        return f"salesai:session:{session_id}:transcript"

    def save_transcript(self, session_id: str, text: str) -> None:
        value = json.dumps({
            "speaker": "unknown",
            "text": text,
        })
        key = self._key(session_id)

        if self.redis_available:
            try:
                self.client.rpush(key, value)
                return
            except (redis.RedisError, OSError):
                self.redis_available = False

        self._memory_store.setdefault(key, []).append(value)

    def get_transcript(self, session_id: str) -> list:
        key = self._key(session_id)

        if self.redis_available:
            try:
                values = self.client.lrange(key, 0, -1)
                return [json.loads(value) for value in values]
            except (redis.RedisError, OSError):
                self.redis_available = False

        return [
            json.loads(value)
            for value in self._memory_store.get(key, [])
        ]

    def clear_session(self, session_id: str) -> None:
        key = self._key(session_id)

        if self.redis_available:
            try:
                self.client.delete(key)
            except (redis.RedisError, OSError):
                self.redis_available = False

        self._memory_store.pop(key, None)
