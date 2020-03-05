import numpy as np

class DataSampleGenerator():

    def __init__(self, eeg, labels, samplingRate, timeSegmentLen,
                 overlap, labelSegmentLen, startCutoff=0, endCutoff=0):
        self.samplingRate = samplingRate
        self.timeSegmentLen = timeSegmentLen
        self.overlap = overlap
        self.labelSegmentLen = labelSegmentLen
        self.startCutoff = startCutoff
        self.endCutoff = endCutoff
        labels = self.fix_labels(labels)
        self.eeg, self.labels = self.clean_data(eeg, labels)


    def __iter__(self):
        return self.sample_generator(self.eeg, self.labels, self.samplingRate,
                                     self.timeSegmentLen, self.overlap,
                                     self.labelSegmentLen, self.startCutoff,
                                     self.endCutoff)
        

    def fix_labels(self, labels):
        """
        Kenan's Magnum Opus (set all label channels to zero
        until it reaches a zero label)
        """
        for label in labels:
            i = 0
            while label[i] != 0:
                label[i] = 0
                i += 1
        return labels


    def clean_data(self, data, labels):
        """
        Removes all data prior to first label.
        """
        for i in range(data.shape[1]):
            if labels[:,i].any():
                return data[:,i:], labels[:,i:]


    def sample_generator(self, data, labels, samplingRate,
                        timeSegment, overlap, labelSegmentLen,
                        startCutoff, endCutoff):
        """
        Generates a sample of data with label.
        --> Parameters in seconds EXCEPT sampingRate and Cutoffs!!!
        """

        index = 0 + startCutoff
        index_end = index + samplingRate * labelSegmentLen -\
                    endCutoff - startCutoff
        while index_end <= data.shape[1]:
            label = np.argmax(labels[:,index])
            segment = data[:,index:index_end]
            segmentJump = timeSegment - overlap
            for actualSegment in self.get_actual_sample(segment, 
                                                        segmentJump,
                                                        timeSegment=timeSegment,
                                                        samplingRate=samplingRate):
                yield actualSegment, label
            index = index_end + 1 + endCutoff
            try:
                while not labels[:,index].any():
                    index += 1
            except IndexError:
                break
            index += startCutoff
            index_end = index + samplingRate * labelSegmentLen - endCutoff - startCutoff

        
    def get_actual_sample(self, segment, segmentJump, timeSegment=3, samplingRate=256):
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
