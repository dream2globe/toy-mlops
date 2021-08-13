import logging
from kafka import KafkaConsumer
from json import loads

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

consumer = KafkaConsumer(
    'mlops',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest', enable_auto_commit=True,
    group_id='serving',
    value_deserializer=lambda x: loads(x.decode('utf-8')),
    consumer_timeout_ms=1_000
)


if __name__ == "__main__":
    try:
        while True:
            for message in consumer:
                logger.info("Topic: %s, Partition: %d, Offset: %d, Key: %s, Value: %s" % (message.topic, message.partition, message.offset, message.key, message.value))
    except KeyboardInterrupt:
        logger.info(f"stopped by a user")
    finally:
        consumer.close()