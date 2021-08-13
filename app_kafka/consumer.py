import logging
import io
import json
import joblib
from pathlib import Path
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

def predict(msg):
    # 변수
    current_max = 0
    best_acc_index = 0

    # 최고 성능 모델 찾기
    model_path = Path("/home/shyeon/workspace/python/toy-mlops/models")
    model_files = list(model_path.glob("*"))

    for i, f_name in enumerate(model_files):
        acc = float(str(f_name)[:-4].split("_")[-1])
        current_max = max(acc, current_max)
        best_acc_index = i

    # 모델 불러오기
    best_model = model_files[best_acc_index]
    model = joblib.load(best_model)
    x = [[v for _, v in msg.items()]]
    return model.predict(x)


if __name__ == "__main__":
    try:
        while True:
            for message in consumer:
                logger.info("Topic: %s, Partition: %d, Offset: %d, Key: %s, Value: %s" % (message.topic, message.partition, message.offset, message.key, message.value))
                # logger.info(f"Predict: {predict(message.value)}")
    except KeyboardInterrupt:
        logger.info(f"stopped by a user")
    finally:
        consumer.close()