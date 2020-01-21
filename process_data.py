from scipy.io import loadmat
import matplotlib.pyplot as plt
import numpy as np
from time import time

# Hz
offset = 0
# Hz
samplingRate = 256
# seconds
timeSegment = 3

def fix_labels(labels):
    """
    Kenans Magnum Opus
    """
    for label in labels:
        i = 0
        while label[i] != 0:
            label[i] = 0
            i += 1
    return labels

def clean_data(data, labels):
    """
    Removes all data prior to first label.
    """
    for i in range(data.shape[1]):
        if labels[:,i].any():
            return data[:,i:], labels[:,i:]

def sample_generator(data, labels, samplingRate=256,
                     timeSegment=3, overlap=2, labelSegmentLen=4,
                     startCutoff=0, endCutoff=0):
    """
    Generates a sample of data with label.
    --> Parameters in seconds EXCEPT sampingRate and Cutoffs!!!
    """
    index = 0 + startCutoff
    index_end = index + samplingRate * labelSegmentLen - endCutoff - startCutoff
    while index_end <= data.shape[1]:
        label = np.argmax(labels[:,index])
        segment = data[:,index:index_end]
        segmentJump = timeSegment - overlap
        for actualSegment in get_actual_sample(segment, segmentJump, timeSegment=timeSegment, samplingRate=samplingRate):
            yield actualSegment, label
        index = index_end + 1 + endCutoff
        try:
            while not labels[:,index].any():
                index += 1
        except IndexError:
            break
        index += startCutoff
        index_end = index + samplingRate * labelSegmentLen - endCutoff - startCutoff
    
def get_actual_sample(segment, segmentJump, timeSegment=3, samplingRate=256):
    """
    Helper function for sample_generator(...):
        Generates samples from found time segment.
    """
    index = 0
    endIndex = timeSegment * samplingRate
    while endIndex <= segment.shape[1]:
        yield segment[:,index:endIndex]
        #yield segment[:,index:endIndex]
        index += segmentJump * samplingRate
        endIndex += segmentJump * samplingRate


if __name__ == '__main__':
    data = loadmat('data/BP_2019PP1.mat')['data'].T
    eeg = data[:6,:]
    labels = data[8:12,:]

    labels = fix_labels(labels)
    eeg, labels = clean_data(eeg, labels)

    startTime = time()
    for sample, label in sample_generator(eeg, labels):
        print(sample.shape, label)
    print(time() - startTime)