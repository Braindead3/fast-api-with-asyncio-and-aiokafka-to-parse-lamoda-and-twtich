from fastapi import HTTPException, status

from src.domain.models.streamer import Streamer, UpdateStreamer
from src.infrastructure.streamer_mongo_repository import StreamerRepository


class StreamerService:

    def __init__(self, streamer_repo: StreamerRepository):
        self._streamer_repo = streamer_repo

    def get_all_streamer(self) -> list[Streamer]:
        return self._streamer_repo.get_all()

    def get_streamer_by_id(self, streamer_id: int) -> Streamer:
        streamer = self._streamer_repo.get({'_id': streamer_id})
        if streamer:
            return streamer
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Streamer ID is does not exists')

    def get_streamer_by_user_name(self, user_name: str) -> Streamer:
        steamer = self._streamer_repo.get({'user_name': user_name})
        if steamer:
            return steamer
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Steamer is does not exists')

    def create_streamer(self, streamer: Streamer) -> Streamer:
        if not self._streamer_repo.get({'_id': streamer.id}):
            return self._streamer_repo.create(streamer)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Streamer already exists')

    def update_streamer(self, streamer: UpdateStreamer) -> Streamer:
        if not self._streamer_repo.get({'_id': streamer.id}):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Streamer does not exists')
        return self._streamer_repo.update(streamer)

    def delete_streamer(self, streamer_id: int) -> {}:
        if not self._streamer_repo.get({'_id': streamer_id}):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Streamer does not exists')

        return self._streamer_repo.delete({'_id': streamer_id})

    def delete_all_streamers(self) -> {}:
        return self._streamer_repo.delete_all()

    def get_page(self, skip: int, limit: int):
        return self._streamer_repo.get_page(limit, skip)
