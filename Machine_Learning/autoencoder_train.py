import numpy as np
import pandas as pd
from keras import Input, Model, layers
import matplotlib as plt

dataset = pd.read_csv("clean_data.csv")
x_train = dataset.to_numpy()
x_train = x_train[:,0:3]

input_dim = 3
latent_dim = 1

input_layer = Input(shape=(input_dim,))
encoded = layers.Dense(2, activation='relu')(input_layer)
encoded = layers.Dense(latent_dim, activation='sigmoid')(encoded)

decoded = layers.Dense(2, activation='relu')(encoded)
decoded = layers.Dense(input_dim, activation='sigmoid')(decoded)

autoencoder = Model(input_layer, decoded)

autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

autoencoder.fit(x_train, x_train,
                epochs=500,
                batch_size=None,
                shuffle=True,
                )

encoder = Model(input_layer, encoded)

compressed_data = encoder.predict(x_train)
wellness_score = compressed_data*100
