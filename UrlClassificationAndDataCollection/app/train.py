import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

app = os.path.abspath(os.path.join(__file__, os.pardir))
PROJ_PATH = os.path.abspath(os.path.join(app, os.pardir))
TEMPLATES_DIR = os.path.join(PROJ_PATH,'templates')
APP_DIR = os.path.join(TEMPLATES_DIR,'app')
DATA_PATH = os.path.join(APP_DIR,'Dataset.arff')
MODEL_PATH = os.path.join(APP_DIR,'random_forest.pkl')

labels = []
data_file = open(DATA_PATH).read()
data_list = data_file.split('\n')
data = np.array(data_list)
data1 = [i.split(',') for i in data]
data1 = data1[0:-1]
for i in data1:
    labels.append(i[30])
data1 = np.array(data1)
features = data1[:, :-1]
# Choose only the relevant features from the data set.
features = features[:, [0, 1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 13, 14, 15, 16, 17, 22, 23, 24, 25, 27, 29]]
features = np.array(features).astype(np.float)

features_train = features
labels_train = labels
# features_test=features[10000:]
# labels_test=labels[10000:]


print("\n\n ""Random Forest Algorithm Results"" ")
clf4 = RandomForestClassifier(min_samples_split=7, verbose=True)
clf4.fit(features_train, labels_train)
importances = clf4.feature_importances_
std = np.std([tree.feature_importances_ for tree in clf4.estimators_], axis=0)
indices = np.argsort(importances)[::-1]
# Print the feature ranking
print("Feature ranking:")
for f in range(features_train.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

# pred4=clf4.predict(features_test)
# print(classification_report(labels_test, pred4))
# print 'The accuracy is:', accuracy_score(labels_test, pred4)
# print metrics.confusion_matrix(labels_test, pred4)

# sys.setrecursionlimit(9999999)
joblib.dump(clf4, MODEL_PATH , compress=9)
