import numpy as np
import pandas as pd
from keras import Input, Model, layers
import matplotlib as plt
from sklearn.preprocessing import MinMaxScaler

dataset = pd.read_csv("Correlated_simulated_data.csv") # Import data generated from correlated multivariate Gaussian distribution
X_train = dataset.to_numpy()
X_train = X_train[:,1:4]
scaler = MinMaxScaler() # Normalises each feature to lie between 0 and 1
scaler.fit(X_train)
X_train = scaler.transform(X_train)

input_dim = 3
latent_dim = 1

input_layer = Input(shape=(input_dim,))
encoded = layers.Dense(2, activation='relu')(input_layer)
encoded = layers.Dense(latent_dim, activation='sigmoid')(encoded) # Sigmoid activation function ensures latent variable lies between 0 and 1

decoded = layers.Dense(2, activation='relu')(encoded)
decoded = layers.Dense(input_dim, activation='sigmoid')(decoded)

autoencoder = Model(input_layer, decoded)

autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

autoencoder.fit(X_train, X_train,
                epochs=500,
                batch_size=None,
                shuffle=True,
                )

encoder = Model(input_layer, encoded)

compressed_data = encoder.predict(X_train)
wellness_score = 100 - compressed_data*100 # Multiply by 100 to get a percentage. Subtract from 100 so that score is positively correlated with wheelchair usage.
