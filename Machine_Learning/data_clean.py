import pandas as pd
import numpy as np

# Load the data from CSV file
PATH_TO_FILE = "C:/Users/relic/Documents/School/Engineering_Cam/Part IIA/3GM1/Machine_Learning/Fake_Autoencoder_Data.csv"

#df = pd.read_csv("Fake_Autoencoder_Data.csv")
df = pd.read_csv(PATH_TO_FILE)

# Calculate some features for each column
df['max_distance_7days'] = df['Distance travelled in meters/day'].rolling(window=7).max()
df['min_distance_7days'] = df['Distance travelled in meters/day'].rolling(window=7).min()
df['mean_distance_7days'] = df['Distance travelled in meters/day'].rolling(window=7).mean()
df['variance_distance_7days'] = df['Distance travelled in meters/day'].rolling(window=7).var()

df['max_duration_7days'] = df['Duration on wheelchair in minutes/day'].rolling(window=7).max()
df['min_duration_7days'] = df['Duration on wheelchair in minutes/day'].rolling(window=7).min()
df['mean_duration_7days'] = df['Duration on wheelchair in minutes/day'].rolling(window=7).mean()
df['variance_duration_7days'] = df['Duration on wheelchair in minutes/day'].rolling(window=7).var()

df['max_distance_from_home_7days'] = df['Distance from home (average)/day'].rolling(window=7).max()
df['min_distance_from_home_7days'] = df['Distance from home (average)/day'].rolling(window=7).min()
df['mean_distance_from_home_7days'] = df['Distance from home (average)/day'].rolling(window=7).mean()
df['variance_distance_from_home_7days'] = df['Distance from home (average)/day'].rolling(window=7).var()

# Fill NaN values with appropriate values
df = df.fillna(method='bfill')

# Save the dataframe to a new CSV file
df.to_csv('clean_data.csv', index=False)

print(df)
