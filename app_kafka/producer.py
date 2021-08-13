from kafka import KafkaProducer
import json
from data import get_data
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

def get_partition(key, all, available):
    return 1 # 파티션을 특정할 수 있음

producer = KafkaProducer(
    bootstrap_servers=["192.168.0.2:9092"],
    value_serializer=json_serializer,
    # compression_type='snappy',
    partitioner=get_partition
)


if __name__ == "__main__":
    try:
        while True:
            msg = get_data()
            logger.info(f"send message: {msg}")
            producer.send("mlops", msg)
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info(f"stopped by a user")
    finally:
        producer.close()
