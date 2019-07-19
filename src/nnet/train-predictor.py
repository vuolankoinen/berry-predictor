import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
# from keras.utils import plot_model

######
# Prepare the data

years = list(range(1990, 2019))

data = pd.read_csv('../../data/Pello-kk-1989-2019-kk.csv')
data.columns = ['year', 'month', 'x1', 'x2', 'x3', 'rain', 'T']
data = data[['year', 'month', 'rain', 'T']]

# Variables are rain and temperature for the preceeding months and the berry sales of the preceeding months.
X_Lappi = pd.DataFrame(columns =
list(map(lambda x : x+"T", map(str, range(1,9)))) +
list(map(lambda x : x+"T-prev", map(str, range(5,13)))) +
list(map(lambda x : x+"R", map(str, range(1,9)))) +
list(map(lambda x : x+"R-prev", map(str, range(5,13))))
)

for ye in years:
    new = []
    for mo in range(1,9):
        new += list(data[data['year'] == ye][data['month'] == mo][['T']].iloc[0])
    for mo in range(5,13):
        new += list(data[data['year'] == ye-1][data['month'] == mo][['T']].iloc[0])
    for mo in range(1,9):
        new += list(data[data['year'] == ye][data['month'] == mo][['rain']].iloc[0])
    for mo in range(5,13):
        new += list(data[data['year'] == ye-1][data['month'] == mo][['rain']].iloc[0])
    X_Lappi.loc[ye-1990] = new
X_Lappi['year'] = years
X_Lappi.set_index('year', inplace = True)
print(X_Lappi)
X_Lappi.fillna(X_Lappi.mean(), inplace = True) # Fill in missing values with means.
Y = pd.read_csv('../../data/berries-sales-volumes.csv')
Y.set_index('year', inplace = True)
Y = Y['lingonberry-Lapland']
Y = Y[years]
mean_Y = np.mean(Y)
Y = Y / mean_Y

# X_Lappi.mean().to_csv('../../data/column-means.csv')
F = X_Lappi.mean()
print(F)
F = F.to_frame()
F.to_csv('../../data/column-means.csv')
print('***')
print(F)

####
# Build the neural net
# First let us do this blindly and just throw all the data at the net without any thought towards what might not be relevant.
net = Sequential()
net.add(Dense(16, input_dim = 32))
net.add(Activation(activation = 'sigmoid'))
net.add(Dense(12))
net.add(Activation(activation = 'relu'))
net.add(Dense(1))
net.add(Activation(activation = 'linear'))
net.compile(optimizer = 'AdaGrad', loss = 'mse')

# Train the neural net
net.fit(X_Lappi, Y, epochs = 1000)
net.summary()

# Save the net
net.save("Lingonberry-Lapland.net")

# Print the results on training data
for ye in years:
    print("Year ", ye, ": prediction ", np.round(net.predict(np.array(X_Lappi.loc[ye:ye]))[0][0]*mean_Y, decimals = 1), ", true amount ", Y[ye]*mean_Y, ".", sep="")

