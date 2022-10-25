from pydantic import BaseSettings


class Mongo(BaseSettings):
    port: int
    host: str

    class Config:
        env_prefix = 'MONGO_'
        env_file = '.env'
        env_file_encoding = 'utf-8'


class Server(BaseSettings):
    port: int
    host: str
    reload: bool

    class Config:
        env_prefix = 'SERVER_'
        env_file = '.env'
        env_file_encoding = 'utf-8'


class Zookeeper(BaseSettings):
    client_port: int
    tick_time: int

    class Config:
        env_prefix = 'ZOOKEEPER_'
        env_file = '.env'
        env_file_encoding = 'utf-8'


class Kafka(BaseSettings):
    broker_id: int
    zookeeper_connect: str
    advertised_listeners: str
    listener_security_protocol_map: str
    inter_broker_listener_name: str
    offsets_topic_replication_factor: int
    auto_create_topics_enable: bool

    class Config:
        env_prefix = 'KAFKA_'
        env_file = '.env'
        env_file_encoding = 'utf-8'


class Config(BaseSettings):
    server: Server = Server()
    mongo: Mongo = Mongo()
    zookeeper: Zookeeper = Zookeeper()
    kafka: Kafka = Kafka()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
