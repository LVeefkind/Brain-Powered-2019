from .dataSampleGenerator import DataSampleGenerator

class FeatureGenerator(DataSampleGenerator):
    
    def __init__(self, eeg, labels, samplingRate, timeSegmentLen,
                 overlap, labelSegmentLen, startCutoff=0, endCutoff=0, args=None):
        super().__init__(eeg, labels, samplingRate,
                         timeSegmentLen, overlap, labelSegmentLen,
                         startCutoff=startCutoff, endCutoff=endCutoff)
        self.args = args
        

    def __iter__(self):
        for iterable in super().__iter__():
            yield iterable