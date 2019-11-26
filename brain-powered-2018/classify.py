#! /usr/bin/env python3
# EEG power classifier and visualizer
# By Derk Barten and Devin Hillenius
# UvA Brain Powered 2017-2018

from sklearn.neighbors import KNeighborsClassifier
from analysis import  plot
# from matplotlib import pyplot

import numpy as np
import argparse
import os

# Global variable because it is hard to pass on argument with function pointer
KNN = None

def on_click(event):
    x = event.xdata
    y = event.ydata
    if x is None or y is None or KNN is None:
        return

    prediction = KNN.predict([[x, y]])
    print("{} {}:\t{}".format(x, y, prediction))


def create_knn_classifier(results):
    
    """ Create a KNN classifier """
    # # List of data points
    # X = []
    # # List of corresponding labels
    # Y = []
    # The first label
    i = 0
    pre_cue_time = round(0.1*256)

    pre_cue_channels = []

    for channel in [0,1]:
        pre_cue_per_channel = []
        for entry in results:
            pre_cue = entry[channel][:pre_cue_time]
            pre_cue_per_channel.append(pre_cue)
        pre_cue_channels.append(np.average(pre_cue_per_channel))

    ms1 = round(0.4*256)
    ms2 = round(0.65*256)
    # p_list = []

    # l = 0
    # Transform the format of the data to one readable by K-Nearest-Neighbors (KNN)
    
    new_array = []
    for entry in results:
        temp = []
        
        #per channel pak je de ms1 tot ms2e getallen
    
        temp.extend(entry[2][ms1:ms2] - pre_cue_channels[0])
        temp.extend(entry[4][ms1:ms2] - pre_cue_channels[1])
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
            continue
            #entry[-1] = 1  
        if len(test_data) < 15:
            test_data.append(entry)
            
        else:
            training_data.append(entry)
        
    test_data = np.array(test_data)
    training_data = np.array(training_data)
    Xt = training_data.T[0]


    Yt = training_data.T[1]


    
    Ytt = []
    for element in Yt:
        Ytt.append(element)

    Xtt = []
    for element in Xt:
        Xtt.append(list(element))

    # print(Xtt[0])


    KNN = KNeighborsClassifier(n_neighbors=5)
    # clf = GradientBoostingClassifier()
    KNN.fit(Xtt, Ytt) 

    # Create the KNN model and fit on the data
    # KNN = KNeighborsClassifier(n_neighbors=7)
    # KNN.fit(X, Y)

    return KNN


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Visualize eeg readings using \
    python scatterplots. The script uses folders as a representation of \
    conditions. Every folder must contain two channels, c1.mat and c2.mat. ')
    # Specify folder
    parser.add_argument('folder', nargs='+', help='Select folders to \
    compare. Each folder must contain both a c1.mat and \
    c2.mat.')
    # Specify sample rate
    parser.add_argument('-s', '--sample_rate', help='Specify the sample rate \
    of the measurement', type=int, default=256)
    # Specify frequency range
    parser.add_argument('-b', '--band', nargs=2, type=int, help="Specify the \
    frequency band in Hz, for example \'--band 8 13\'", default=[8, 13])
    # Specify the length of the signal in seconds
    parser.add_argument('-l', '--length', type=float, help="Specify the \
    length of the signal to process, for example \'--length 1.5\' to only \
    process the first one and a half seconds of the signal. If the specified \
    length is longer than the length of the signal, the whole signal is used.")

    args = parser.parse_args()
    folders = args.folder
    band = args.band
    sample_rate = args.sample_rate
    length = args.length

    results = run_analysis(folders, band, sample_rate, length)
    KNN = create_knn_classifier(results)

    # Create an interactive plot
    plot(results, sample_rate, band, callback=on_click)
    exit(0)
