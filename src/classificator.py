import csv

from utilities.watcher import *
import utilities.csvGenerator as generate
import utilities.data as data
import src.preProcessing as pp

from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.linear_model import *
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

algorithmDict = {
  'decisionTree': DecisionTreeClassifier(),
  'randomForest': RandomForestClassifier(n_estimators=100),
  'svc' : SVC(kernel='linear', C=10.0, random_state=1),
  'naiveBayes': GaussianNB(),
  'knn': KNeighborsClassifier(),
  'logisticRegression' : LogisticRegression(C=10000, solver='liblinear')
}

def classification(x_train, y_train, x_test, y_test, algorithm='randomForest', decompositor=''):
  ctx= algorithm.upper()+'-MACHINE LEARNING CLASSIFICATION'
  start= watcherStart(ctx)

  model = algorithmDict[algorithm]
  model.fit(x_train, y_train)
  predictionResult = model.predict(x_test)
  tn, fp, fn, tp = confusion_matrix(y_test, predictionResult).ravel()

  print('\nTotal input data\t\t\t\t: '+str(x_test.shape[0]))
  print('TN (predict result normal, actual normal)\t: '+str(tn))
  print('FP (predict result bot, actual normal)\t\t: '+str(fp))
  print('FN (predict result normal, actual bot)\t\t: '+str(fn))
  print('TP (predict result bot, actual bot)\t\t: '+str(tp))

  decompositor = decompositor if decompositor != '' else 'None'
  generate.classificationResult(algorithm, decompositor, tn, fp, fn, tp)
  
  watcherEnd(ctx, start)
  return predictionResult

def executor(raw_df, algorithm='randomForest', decompositor=''):
  if decompositor!='':
    raw_df = pp.dimentionalReduction(decompositor, 1, raw_df)

  train, test = data.splitTestAllDataframe(raw_df)
  categorical_features=[feature for feature in raw_df.columns if (
    raw_df[feature].dtypes=='O' or feature =='SensorId' or feature =='ActivityLabel'
  )]

  print(raw_df)

  # y_train = train['ActivityLabel']
  # y_test = test['ActivityLabel']

  # if decompositor=='':
  #   x_train = train.drop(categorical_features, axis=1)
  #   x_test = test.drop(categorical_features, axis=1)
  # else:
  #   x_train = train[['DimRedFeature']]
  #   x_test = test[['DimRedFeature']]

  # classification(x_train, y_train, x_test, y_test, algorithm, decompositor)