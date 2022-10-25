from src.domain.models.streamer import Streamer, UpdateStreamer
from src.infrastructure.base_repositroy import BaseRepository


class StreamerRepository(BaseRepository[Streamer, UpdateStreamer]):
    class Meta:
        collection = 'streamers'
