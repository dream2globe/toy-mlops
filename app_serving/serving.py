import io
import joblib
import json
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

class Item(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


app = FastAPI()
model = None

@app.post("/")
def create_item():
	return "Running the prediction service"


@app.post("/pred/")
def predict(item: Item):
    # 변수
    current_max = 0
    best_acc_index = 0

    # 최고 성능 모델 찾기
    model_path = Path("./models")
    model_files = list(model_path.glob("*"))

    for i, f_name in enumerate(model_files):
        acc = float(str(f_name)[:-4].split("_")[-1])
        current_max = max(acc, current_max)
        best_acc_index = i

    # 모델 불러오기
    best_model = model_files[best_acc_index]
    print(best_model)
    jmsg = json.load(io.StringIO(item.json()))
    model = joblib.load(best_model)
    x = [[v for _, v in jmsg.items()]]
    print("Prediction result is", model.predict(x))

    return None

