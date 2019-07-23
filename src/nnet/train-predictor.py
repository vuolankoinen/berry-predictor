import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
# from keras.utils import plot_model

######
# Prepare the input data, i.e. the meteorological observations

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
    for mo in range(1, 9):
        new += list(data[data['year'] == ye][data['month'] == mo][['T']].iloc[0])
    for mo in range(5, 13):
        new += list(data[data['year'] == ye - 1][data['month'] == mo][['T']].iloc[0])
    for mo in range(1, 9):
        new += list(data[data['year'] == ye][data['month'] == mo][['rain']].iloc[0])
    for mo in range(5, 13):
        new += list(data[data['year'] == ye - 1][data['month'] == mo][['rain']].iloc[0])
    X_Lappi.loc[ye - 1990] = new
X_Lappi['year'] = years
X_Lappi.set_index('year', inplace = True)
print(X_Lappi)
X_Lappi.fillna(X_Lappi.mean(), inplace = True) # Fill in missing values with means.
F = X_Lappi.mean()
F = F.to_frame()
F.to_csv('../../data/inputs-column-means.csv')

######
# Prepare the output data, i.e. the berry sales

def sales_data(berry, area, years=list(range(1990, 2019))):
    Y = pd.read_csv('../../data/berries-sales-volumes.csv')
    Y.set_index('year', inplace = True)
    Y = Y[berry + '-' + area]
    Y = Y[years]
    mean_Y = np.mean(Y)
    Y = Y / mean_Y
    f = open('../../data/mean-' + berry + '-' + area + '.dat', 'w')
    f.write(str(mean_Y))
    f.close()
    return Y

####
# Build and train the neural net
def build_net(X, Y):
    net = Sequential()
    net.add(Dense(16, input_dim = 32))
    net.add(Activation(activation = 'sigmoid'))
    net.add(Dense(12))
    net.add(Activation(activation = 'relu'))
    net.add(Dense(1))
    net.add(Activation(activation = 'linear'))
    net.compile(optimizer = 'AdaGrad', loss = 'mse')

    # Train the neural net
    net.fit(X, Y, epochs = 1000)
    return net


Y_ll = sales_data('lingonberry', 'lapland')
build_net(X_Lappi, Y_ll).save("lingonberry-lapland.net")

Y_cl = sales_data('cloudberry', 'lapland')
build_net(X_Lappi, Y_cl).save("cloudberry-lapland.net")

Y_bl = sales_data('blueberry', 'lapland')
build_net(X_Lappi, Y_bl).save("blueberry-lapland.net")
