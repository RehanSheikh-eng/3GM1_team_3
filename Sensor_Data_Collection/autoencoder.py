import numpy as np
import pandas as pd
from keras import Input, Model, layers
import matplotlib as plt

decoding_dim = 12 # Expanded features (avg, var, min, max) of daily distance travelled, duration on wheelchair, distance from home
encoding_dim = 1 # Holistic Wellness Score

input_layer = Input(shape=(decoding_dim,))
encoded = layers.Dense(8, activation='relu')(input_layer)
encoded = layers.Dense(4, activation='relu')(encoded)

decoded = layers.Dense(4, activation='relu')(encoded)
decoded = layers.Dense(8, activation='relu')(decoded)
decoded = layers.Dense(decoding_dim, activation='sigmoid')(decoded)

# Autoencoder model
autoencoder = Model(input_layer, decoded)

# Encoder model
encoder = Model(input_layer, encoded)

# Decoder model
encoded_input = Input(shape=(encoding_dim,))
decoder_layer = autoencoder.layers[-1]
decoder = Model(encoded_input, decoder_layer(encoded_input))

autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

autoencoder.fit(x_train, x_train,
                epochs=50,
                batch_size=256,
                shuffle=True,
                # validation_data=(x_test, x_test)
                )

encoded_data = encoder.predict(x_test)
decoded_data = decoder.predict(encoded_data)