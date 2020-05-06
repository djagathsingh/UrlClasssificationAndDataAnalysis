from app import feature_extraction
import numpy as np
import joblib
import sys
import os

app = os.path.abspath(os.path.join(__file__, os.pardir))
PROJ_PATH = os.path.abspath(os.path.join(app, os.pardir))
TEMPLATES_DIR = os.path.join(PROJ_PATH,'templates')
APP_DIR = os.path.join(TEMPLATES_DIR,'app')
DATA_PATH = os.path.join(APP_DIR,'Dataset.arff')
MODEL_PATH = os.path.join(APP_DIR,'random_forest.pkl')

def predictions(test_url):
    features_test = feature_extraction.main(test_url)
    # Due to updates to scikit-learn, we now need a 2D array as a parameter to the predict function.
    features_test = np.array(features_test).reshape((1, -1))

    clf = joblib.load(MODEL_PATH)

    pred = clf.predict(features_test)
    return int(pred[0])
