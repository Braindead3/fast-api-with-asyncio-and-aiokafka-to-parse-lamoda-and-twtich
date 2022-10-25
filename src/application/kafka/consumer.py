import asyncio

from aiokafka import AIOKafkaConsumer

from main import db_client
from src.application.parsers.twtich_parser import TwitchParser
from src.application.streamer_service import StreamerService
from src.infrastructure.streamer_mongo_repository import StreamerRepository

streamer_service = StreamerService(StreamerRepository(db_client))

parser = TwitchParser()


async def consume_msg(consumer: AIOKafkaConsumer) -> None:
    try:
        async for msg in consumer:
            asyncio.create_task(parser.parse(streamer_service))
    finally:
        await consumer.stop()
