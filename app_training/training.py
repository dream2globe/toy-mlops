import pandas as pd
import logging
import joblib
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


if __name__ == "__main__":

    # data loading
    logger.info(f"loading data")
    iris = load_iris()
    iris_data = iris.data
    iris_label = iris.target

    # preprocessing
    df_iris = pd.DataFrame(data=iris_data, columns=iris.feature_names)
    df_iris['label'] = iris.target

    # training
    logger.info(f"training")
    x_train, x_test, y_train, y_test = train_test_split(iris_data, iris_label, test_size=0.2, random_state=11)
    clf = DecisionTreeClassifier(random_state=11)
    clf.fit(x_train, y_train)
    pred = clf.predict(x_test)

    # reporting
    acc = accuracy_score(y_test, pred)
    logger.info(f'accuracy score: {acc}')

    # saving
    joblib.dump(clf, f"/home/shyeon/workspace/python/toy-mlops/models/df_{acc:.3f}.pkl") 
