import numpy as np
import matplotlib.pyplot as plt

def data_loader(file):
    """
    Loads file from given filepath.

    file: path to file
    """
    pass

def parse_data(data):
    """
    Parse data to correct format (numpy array?)

    data: data to parse
    """
    pass

def sample_generator(data, windowLength, offset=0):
    """
    Generates samples samples from data from length windowLength by 
    scanning the data from left to right. 

    data: data to generate sampels from
    windowLength: size of window of generated sample in amount of samples
    offset: jumpsize of scanning window (default = 1)
    """

    # Pad data with zeros 
    padding = data.size % windowLength
    dataMatrix = np.zeros((data.size + padding))
    dataMatrix[:data.size] = data

    # Generate sampels of size windowLength
    i = 0
    while i + windowLength <= dataMatrix.size:
        yield dataMatrix[i:i + windowLength] 
        i += 1 + offset

if __name__ == "__main__":
    data_test = np.arange(37)
    windowLength = 3
    for sample in sample_generator(data_test, windowLength, offset=1):
        print(sample)