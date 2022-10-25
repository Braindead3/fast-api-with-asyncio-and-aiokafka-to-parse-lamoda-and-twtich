import pymongo
import uvicorn

from src.config import config

db_client = pymongo.MongoClient(config.mongo.host, config.mongo.port)

if __name__ == '__main__':
    uvicorn.run(
        app='app:app',
        port=config.server.port,
        host=config.server.host,
        reload=config.server.reload
    )
