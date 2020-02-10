import scipy.io as sio
import os, glob
import numpy as np
import sys
import pandas as pd

from scipy import spatial
# import mne
from scipy.fftpack import fft, ifft
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import NuSVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from scipy.fftpack import fft

 
data = np.load('Klaas.npy',allow_pickle=True).T

channels = data[:2]

pre_cue_time = round(0.1*256)

pre_cue_channels = []

for channel in range(6):
    pre_cue_per_channel = []
    for entry in data:
        pre_cue = entry[channel][:pre_cue_time]
        pre_cue_per_channel.append(pre_cue)
    pre_cue_channels.append(np.average(pre_cue_per_channel))


ms1 = round(0.4*256)
ms2 = round(0.65*256)
p_list = []

l = 0
# for g in range(6):/
for j in range(6):
	for k in range(6):
		total = 0
		for i in range(50):
			new_array = []
			for entry in data:
				temp = []
				temp2 = []
				
				#per channel pak je de ms1 tot ms2e getallen
			
				temp.extend(entry[j][ms1:ms2] - pre_cue_channels[j])
				temp.extend(entry[k][ms1:ms2] - pre_cue_channels[k])
				# temp.extend(entry[g][ms1:ms2] - pre_cue_channels[g])
				#normaliseren
				normd = temp / np.linalg.norm(temp)


				new_array.append([list(normd),entry[-1]])

			tempd = np.array(new_array)

			np.random.shuffle(tempd)

			test_data = []
			training_data = []
			for entry in tempd:

				if entry[-1] == 2 or entry[-1] == 3:
					entry[-1] = 1  

				if len(test_data) < 15 :
					test_data.append(entry)

				else:
					training_data.append(entry)



			test_data = np.array(test_data)
			training_data = np.array(training_data)

			Xt = training_data.T[0]
			Xf = test_data.T[0]

			Yt = training_data.T[1]
			Yf = test_data.T[1]


			Ytt = []
			for element in Yt:
				Ytt.append(element)

			Xtt = []
			for element in Xt:
				Xtt.append(list(element))

			Xff = []
			Yff = []

			for i in range(len(test_data)):
				Xff.append(list(Xf[i]))
				Yff.append(Yf[i])

			clf = KNeighborsClassifier(n_neighbors=5)
			# clf = GradientBoostingClassifier()
			clf.fit(Xtt, Ytt) 

			accuracy = 0


			p = clf.predict(Xff)


			for i in range(len(p)):
				if p[i] == Yff[i]:
					accuracy+=1

			total += accuracy/len(p)
		l += 1
		print('optie = ',l,' total= ', round(total*2), ' ch1 = ',j, ' ch2 = ',k)
		p_list.append(total/50)
print(np.shape(Xff))

print(max(p_list),p_list.index(max(p_list)) + 1)
