from preprocessor import DataSampleGenerator
from preprocessor import FeatureGenerator
from scipy.io import loadmat

# ~~~~ SAMPLE CODE ~~~~

# Hz
offset = 0
# Hz
samplingRate = 256
# seconds
timeSegmentLen = 3
# overlap
overlap = 2
# seconds
labelSegmentLen = 4
# Hz
startCutoff = 0
endCutoff = 0

# Get the data from the matlab file
data = loadmat('data/BP_2019PP1.mat')['data'].T
# EEG data in following format: 
#   cols = samples, rows = channels
#   channels 6 and 7 contain bad data, so we ignore those
eeg = data[:6,:]
# Last 4 channels are the label channels
labels = data[8:12,:]

# Set up the sample generator:
#   samplingRate    : The current data file has a sampling rate of 256 Hz
#   timeSegmentLen  : We want to generate labeled samples of 3 seconds long
#   overlap         : We want to overlap each sample for two seconds
#   labelSegmentLen : The amount of seconds of data each corresponding to a label
#   startCutoff     : Amount of samples to ignore at the start of each labelSegment
#   endCutoff       : Amount of samples to ignore at the end of each labelSegment  
sampleGenerator = DataSampleGenerator(eeg, labels, samplingRate, timeSegmentLen, overlap,
                                        labelSegmentLen, startCutoff, endCutoff)

# Now we can simply loop over each generated sample + label

for sample, label in sampleGenerator:
    print(sample.shape, label)
    break

# FeatureGenerator is a child of SampleGenerator. 
# It allows for the same parameters to generate samples,
# but allows for more specific alterations to samples such as ICA.
featureGenerator = FeatureGenerator(eeg, labels, samplingRate, timeSegmentLen, overlap,
                                    labelSegmentLen, startCutoff, endCutoff, ["fourier"])

for feature, label in featureGenerator:
    print(feature.shape, label)
    break

