import numpy as np
import pandas as pd
from keras import Input, Model, layers
import matplotlib as plt

dataset = pd.read_csv("clean_data.csv")
x_train = dataset.to_numpy()

input_dim = 15 # Expanded features (avg, var, min, max) of daily distance travelled, duration on wheelchair, distance from home
latent_dim = 1 # Holistic Wellness Score

# input_layer = Input(shape=(input_dim,))
# encoded = layers.Dense(12, activation='relu')(input_layer)
# encoded = layers.Dense(6, activation='relu')(encoded)
# encoded = layers.Dense(latent_dim, activation='relu')(encoded)

# decoded = layers.Dense(6, activation='relu')(encoded)
# decoded = layers.Dense(12, activation='relu')(decoded)
# decoded = layers.Dense(input_dim, activation='sigmoid')(decoded)

# # Autoencoder model
# autoencoder = Model(input_layer, decoded)

# # Encoder model
# encoder = Model(input_layer, encoded)

# # Decoder model
# encoded_input = Input(shape=(latent_dim,))
# decoder_layer = autoencoder.layers[-1]
# decoder = Model(encoded_input, decoder_layer(encoded_input))

# autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

# autoencoder.fit(x_train, x_train,
#                 epochs=1,
#                 batch_size=None,
#                 shuffle=True,
#                 )


# Encoder
encoder_inputs = Input(shape=(input_dim,))
encoder = layers.Dense(latent_dim, activation='relu')(encoder_inputs)

# Decoder
decoder_outputs = layers.Dense(input_dim, activation='sigmoid')(encoder)

# Autoencoder
autoencoder = Model(encoder_inputs, decoder_outputs)

# Compile the model
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

# Train the autoencoder
autoencoder.fit(x_train, x_train, epochs=10, batch_size=None)

# Compress the data using the encoder part of the autoencoder


compressed_data = encoder.predict(x_train)
print(compressed_data)