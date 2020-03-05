from .dataSampleGenerator import DataSampleGenerator
from sklearn.decomposition import FastICA
from scipy import signal

import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack


class FeatureGenerator(DataSampleGenerator):
    # theta - alpha - beta - gamma
    bandFrequencies = [(4, 8), (8, 16), (16, 32), (32, 90)]
    
    def __init__(self, eeg, labels, samplingRate, timeSegmentLen,
                 overlap, labelSegmentLen, startCutoff=0, endCutoff=0, args=None):
        super().__init__(eeg, labels, samplingRate,
                         timeSegmentLen, overlap, labelSegmentLen,
                         startCutoff=startCutoff, endCutoff=endCutoff)

        self.samplingRate = samplingRate
        if "ica" in args:
            # Parameters need refining
            self.ica = FastICA(max_iter=200, tol=0.001)
        self.args = args
        self.bandpass()

        
    def __iter__(self):
        for feature, label in super().__iter__():
            # print("")
            # if "ica" in self.args:
            #     feature = self.ica.fit_transform(feature.T).T
            # if "fourier" in self.args:
            #     feature = self.fourier(feature)
            feature = self.fastFourier(feature)
            feature = self.getAverangeBandPowerValues(feature)
            yield feature, label


    def bandpass(self):
        """
        Applies bandpass filter and necessary mean zeroing.
        """
        sosHigh = signal.butter(20, 1, 'hp', fs=256, output='sos')
        sosLow = signal.butter(20, 40, 'lp', fs=256, output='sos')

        for i, sig in enumerate(self.eeg):
            mean_removed = np.ones_like(sig) * np.mean(sig)
            sig = sig - mean_removed
            sig = signal.sosfilt(sosHigh, sig)
            self.eeg[i] = signal.sosfilt(sosLow, sig)

    
    def getAverangeBandPowerValues(self, feature):
        avgPowerValues = []

        for sample in feature:
            avgPowerValue = []
            for band in self.bandFrequencies:
                avgPowerValue.append(np.mean(sample[band[0]:band[1]]))
            avgPowerValues.append(avgPowerValue)
        
        return np.array(avgPowerValues)




    # N_fft = Number of bins (chooses granularity)
    def fastFourier(self, feature, N_fft=100):
        fft_feature = []

        for sample in feature:
            # Number of samplepoints
            N = sample.shape[0]
            T = 1.0 / self.samplingRate      # N_samps*T (#samples x sample period) is the sample spacing.
               
            # the interval
            x = np.linspace(0, N * T, N)     

            yf = scipy.fftpack.fft(sample, n=N_fft)
            xf = np.arange(0, self.samplingRate, self.samplingRate / N_fft)
            sample = 2.0 / N * np.abs(yf[0: N // 2])
            fft_feature.append(sample[:N_fft // 2])

        return np.array(fft_feature)


    def fourier(self, feature):
        # Currently only performs fourier on the first channel.
        time_step = 1 / self.samplingRate
        ps = np.abs(np.fft.fft(feature[0]))**2
        freqs = np.fft.fftfreq(feature[0].size, time_step)
        idx = np.argsort(freqs)
        # Plotting test
        high = np.argmax(ps)
        print(freqs[high])
        plt.plot(freqs[idx], ps[idx])
        plt.show()
        return feature
