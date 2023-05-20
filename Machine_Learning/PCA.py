import numpy as np
import pandas as pd
from keras import Input, Model, layers
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import math

dataset = pd.read_csv("clean_data.csv")
X = dataset.to_numpy()
X = X[:,0:3]

pca = PCA(n_components=1)
pca.fit(X)

Y = pca.transform(X)

def sigmoid(x):
  return 1 / (1 + np.exp(-x))

Y = sigmoid(Y)*100