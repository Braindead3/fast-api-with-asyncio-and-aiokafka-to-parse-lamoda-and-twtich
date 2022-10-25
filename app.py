import asyncio
from json import loads

from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI

from src.application.kafka.consumer import consume_msg
from src.interface.product_interface import router as product_router
from src.interface.twitch_interface import router as home_router

app = FastAPI()

app.include_router(product_router)
app.include_router(home_router)

consumer = None
consumer_task = None


@app.on_event('startup')
async def startup_event():
    await initialize()
    await consume()


@app.on_event('shutdown')
async def shutdown_event():
    consumer_task.cancel()
    await consumer.stop()


async def initialize():
    global consumer
    consumer = AIOKafkaConsumer(
        'Topic1',
        bootstrap_servers=['kafka:29092'],
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )
    await consumer.start()


async def consume():
    global consumer_task
    consumer_task = asyncio.create_task(consume_msg(consumer))
