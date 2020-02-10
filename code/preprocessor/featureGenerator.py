from .dataSampleGenerator import DataSampleGenerator
from sklearn.decomposition import FastICA
import numpy as np
import matplotlib.pyplot as plt


class FeatureGenerator(DataSampleGenerator):
    
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
        

    def __iter__(self):
        for feature, label in super().__iter__():
            if "ica" in self.args:
                feature = self.ica.fit_transform(feature.T).T
            if "fourier" in self.args:
                feature = self.fourier(feature)
            yield feature, label

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
