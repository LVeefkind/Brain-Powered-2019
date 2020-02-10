import numpy as np
data = np.load('KLAAS.npy', allow_pickle=True)
data[0][0].tofile("data.csv",format='%.4e',sep=',')
