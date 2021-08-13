import math
import matplotlib.pyplot as plt
import numpy as np
import json
from random import randint
from sklearn.datasets import load_iris

data = load_iris()

def get_data():
    length = data["data"].shape[0]
    random_sample = randint(0, length-1)
    message = {k: v for k, v in zip(data["feature_names"], data["data"][random_sample])}
    return message