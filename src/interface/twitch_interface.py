import json
from typing import Optional

from aiokafka import AIOKafkaProducer
from fastapi import Path, Query, APIRouter
from starlette import status

from main import db_client
from src.application.streamer_service import StreamerService
from src.domain.models.streamer import Streamer, UpdateStreamer
from src.infrastructure.streamer_mongo_repository import StreamerRepository

router = APIRouter(tags=['twitch'], prefix='/streamer')

streamer_service = StreamerService(StreamerRepository(db_client))


@router.get('/', response_model=list[Streamer])
async def get_all_streamers() -> list[Streamer]:
    return streamer_service.get_all_streamer()


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def del_all_streamers():
    return streamer_service.delete_all_streamers()


@router.get('/{streamer_id}', response_model=Streamer)
async def get_streamer_by_id(
        streamer_id: int = Path(None, description='The ID of the streamer you would like to view', gt=0)) -> Streamer:
    return streamer_service.get_streamer_by_id(streamer_id)


@router.get('/{user_name}', response_model=Streamer)
async def get_streamer_by_user_name(user_name: Optional[str] = None) -> Streamer:
    return streamer_service.get_streamer_by_user_name(user_name)


@router.post('/', response_model=Streamer)
async def create_streamer(streamer: Streamer) -> Streamer:
    return streamer_service.create_streamer(streamer)


@router.put('/', response_model=Streamer)
async def update_streamer(streamer: UpdateStreamer) -> Streamer:
    return streamer_service.update_streamer(streamer)


@router.delete('/{streamer_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_streamer(streamer_id: int = Path(description='The ID of the streamer to delete')) -> {}:
    return streamer_service.delete_streamer(streamer_id)


@router.get('/parse-all')
async def parse_most_popular_streams() -> dict:
    producer = AIOKafkaProducer(bootstrap_servers=['kafka:29092'],
                                value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    await producer.start()
    try:
        await producer.send_and_wait(topic='Topic1', value='start')
    finally:
        await producer.stop()
    return {'msg': 'start parsing'}


@router.get('/get-page', response_model=list[Streamer])
async def get_page(skip: int = Query(..., description='How much documents do you want to skip'),
                   limit: int = Query(..., description='How much documents do you want to receive')) -> list[Streamer]:
    return streamer_service.get_page(skip, limit)
