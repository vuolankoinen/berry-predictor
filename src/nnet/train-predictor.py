import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
# from keras.utils import plot_model

######
# Prepare the data

years = list(range(1991, 2019))

data = pd.read_csv('../../data/Kittila-Pokka-1990-2019-kk.csv')
data.columns = ['year', 'month', 'x1', 'x2', 'x3', 'rain', 'T']
data = data[['year', 'month', 'rain', 'T']]
# Variables are rain (R) and temperature (T) for each month (1-12):
X_Lappi = pd.DataFrame(columns=list(map(lambda x : x+"T", map(str, range(1,13)))) + list(map(lambda x : x+"R", map(str, range(1,13)))))

for ye in years:
    new = []
    for mo in range(1,13):
        new += list(data[data['year'] == ye][data['month'] == mo][['T']].iloc[0])
    for mo in range(1,13):
        new += list(data[data['year'] == ye][data['month'] == mo][['rain']].iloc[0])
    X_Lappi.loc[ye-1991] = new
X_Lappi['year'] = years
X_Lappi.set_index('year', inplace = True)
X_Lappi.fillna(X_Lappi.mean(), inplace = True) # Fill in missing values with means.
Y = pd.read_csv('../../data/berries-sales-volumes.csv')
Y.set_index('year', inplace = True)
Y = Y['lingonberry-Lapland']
Y = Y[years]

####
# Build the neural net
# First let us do this blindly and just throw all the data at the net without any thought towards what might not be relevant.

net = Sequential()
net.add(Dense(14, input_dim = 24))
net.add(Activation(activation = 'sigmoid'))
net.add(Dense(1))
net.add(Activation(activation = 'sigmoid'))
net.compile(optimizer = 'AdaGrad', loss = 'mse')

# Train the neural net
net.fit(X_Lappi, Y, epochs = 100)
net.summary()

# Save the net
net.save("Lingonberry-Lapland.net")
