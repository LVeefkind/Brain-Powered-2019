import preprocessor
from scipy.io import loadmat

print(preprocessor.dataSampleGenerator.dataSampleGenerator)

# Hz
offset = 0
# Hz
samplingRate = 256
# seconds
timeSegment = 3

if __name__ == '__main__':
    data = loadmat('data/BP_2019PP1.mat')['data'].T
    eeg = data[:6,:]
    labels = data[8:12,:]
    
    sampleGenerator = preprocessor.dataSampleGenerator.dataSampleGenerator(eeg, labels)
    for sample, label in sampleGenerator:
        print(sample.shape, label)