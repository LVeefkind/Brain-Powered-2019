import scipy.io as sio
import numpy as np
data = sio.loadmat('KLAAS.mat')
np.save('klaas.npy', data)


data = np.load('klaas.npy',allow_pickle=True).T
print(data)
