# Try to predict some features
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

def x_y_pairs(nyc_squirrels, prediction_of):

  # shuffle dataset
  nyc_squirrels = nyc_squirrels.sample(frac=1).reset_index(drop=True)

  #labels
  label = nyc_squirrels[prediction_of].values.reshape(-1, 1)
  if "primary" in prediction_of:
    nyc_squirrels_temp = nyc_squirrels.drop(columns=['primary_Unknown', 'primary_Gray', 'primary_Cinnamon', 'primary_Black'], axis=1)
  elif "highlight" in prediction_of:
    nyc_squirrels_temp = nyc_squirrels.drop(columns=['highlight_Unknown', 'highlight_Cinnamon', 'highlight_White',
       'highlight_Gray', 'highlight_Cinnamon, White', 'highlight_Gray, White',
       'highlight_Black, Cinnamon, White', 'highlight_Black',
       'highlight_Black, White', 'highlight_Black, Cinnamon',
       'highlight_Gray, Black'], axis=1)
  elif "lat" in prediction_of or "long" in prediction_of:
    nyc_squirrels_temp = nyc_squirrels.drop(columns=['long', 'lat'], axis=1)
  else:
    nyc_squirrels_temp = nyc_squirrels.drop(columns=prediction_of, axis=1)
  #predictors
  predictors = nyc_squirrels_temp[nyc_squirrels_temp.columns].values

  return predictors, label, nyc_squirrels_temp.columns

def split_data(predictors, label, train_test_ratio = 0.75):
  A = np.split(predictors, [int(len(predictors)*train_test_ratio), int(len(predictors)*train_test_ratio)], axis=0)
  B = np.split(label, [int(len(label)*train_test_ratio), int(len(predictors)*train_test_ratio)],axis=0)
  train_X = A[0]
  test_X = A[2]
  train_Y = B[0]
  test_Y = B[2]
  return train_X, train_Y.ravel(), test_X, test_Y.ravel()

def fit(train_X, train_Y, mod="LogisticRegression"):
  model = LogisticRegression().fit(train_X, train_Y)
  return model

def test_accuracy(model, test_X, test_Y, mod):
  y_pred = model.predict_proba(test_X)
  y_pred = np.argmax(y_pred, axis=1)
  sum = 0
  for i in range(len(y_pred)):
    if y_pred[i] == test_Y[i]:
      sum = sum + 1
  return 100*sum/len(y_pred)
