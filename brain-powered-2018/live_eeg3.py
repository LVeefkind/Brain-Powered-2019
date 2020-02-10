#! /usr/bin/env python3
# Reads live Matlab EEG data
# By Derk Barten and Devin Hillenius
# UvA Brain Powered 2017-2018
# py live_eeg3.py -c "KLAAS.npy" -d "KLA"
# py classifier2.py "KLAAS.npy"
# cd Desktop/UvA_EEG_recorder-master/brain-powered-master

import csv
import pandas as pd
import os
import signal
import time
import itertools
import numpy as np
import analysis
import classify
import pickle
import argparse
import random
from drone import Drone

#LABELS = ['north', 'other']
LABELS = sorted(['north', 'other'])
calibrations_folder = 'calibrations'

# mapping is al aangepast naar onze opties
MAPPING = {'other': 'rotate_right',
           'north': 'forward'}

route_list = [1,1,1]
route_index = 0
#dit ook
NUM_PLOT_CLASSIFICATION = 2

DRONE = None

def handle_signint(signum, frame):
    DRONE.land()

# live inlezen van de data
def read_delete_when_available(filename):
    while not os.path.exists(filename):
        time.sleep(0.05)
    time.sleep(0.1)


    # VERANDER DIT
    data = np.loadtxt(filename, delimiter=",").T
    # data = np.reshape(data,(1,512))[0]
    print(np.shape(data))

    # while True:
    #     try:
    #         os.remove(filename)
    #         break
    #     except:
    #         continue

    return data

# FREESTYLE???
#def periodically_classify(calibration, filename='data.csv'):
#    while True:
#        data = read_delete_when_available(filename)
#        # result = analysis.analysis([data[:,0]], [data[:,1]])
#        # calibration['new'] = [[result[0][0]], [result[1][0]]]
#        prediction = analysis.KNN.predict_proba([[data[0][0], data[1][0]]])
#        label_classification(calibration, prediction)

def periodically_classify(calibration,route_index, route_list, filename='../data.csv'):
    while True:
        ms1 = round(0.4*256)
        ms2 = round(0.65*256)
        data = read_delete_when_available(filename)
        temp = []
        print('ok')

        temp.extend(data[0][ms1:ms2])
        temp.extend(data[1][ms1:ms2])

        print('ok')
        #normaliseren
        normd = temp / np.linalg.norm(temp)

        # FREESTYLE
        prediction = analysis.KNN.predict_proba([normd])
        norma = [list(normd)]

        #normd = normd.reshape(1,-1)
#        print(normd)
#        print(np.shape(normd))

        #prediction = analysis.KNN.predict(normd)
        print('prediction: ' ,prediction)

        #label_classification(prediction[0],route_index,route_list)
        label_classification(calibration, prediction)



# FREESTYLE
def label_classification(calibration, prediction):
    max_prediction = max(prediction[0])
    label = np.argmax(prediction[0])

    print(prediction[0])
    if max_prediction >= 0.6:
        #print("Predicted {} at {} confidence".format(LABELS[label], max_prediction))

        if DRONE != None:
            print("Moving drone!")
            print(MAPPING[LABELS[label]])
            DRONE.move(MAPPING[LABELS[label]])
         # if NUM_PLOT_CLASSIFICATION > 0:
         #     NUM_PLOT_CLASSIFICATION -= 1
         #     show_calibration(calibration)
         # else:
        time.sleep(4)
        return True
    else:
        print("No classification")

    return False

#def label_classification( prediction,route_index,route_list):
#    # fake
#    # pred = ["move_right", "move_forward", "move_forward", "move_forward", "move_forward", "move_forward", "move_forward"]
#    if prediction > 0.6:
#        print("Predicted {}".format(LABELS[prediction]))
#        route_index += 1
#        if DRONE != None:
#            print("Moving drone!")
#
#            # HAAL DIT WEG BIJ BEWEGEN VAN DRONE
#            # fake
#            # print(random.choice(pred))
#            # real
#            print(MAPPING[LABELS[prediction]])
#            # VOEG DIT WEER TOE VOOR BEWEGEN
#            DRONE.move(MAPPING[LABELS[prediction]])




        # IDK WAT DIT IS

        # if NUM_PLOT_CLASSIFICATION > 0:
        #     NUM_PLOT_CLASSIFICATION -= 1
        #     show_calibration(calibration)
        # else:

#        time.sleep(4)
#        return True
#    else:
#        print("No classification")
#    time.sleep(4)

#    return False

# calibreert voor de persoon die live aan de eeg zit op dat moment. Dit betekent dat ie een soort
# test ronde doet en voor elke 'optie' de persoon soort van matcht aan de trainingsdata om te kijken
# of het een beetje klopt. Ik denk dat we dit misschien uberhaupt niet hoeven te doen als we
# van tevoren al weten wie we er aan hangen. Als we dit wel gaan doen moeten we het gecommente
# gedeelte aanpassen
# def calibrate(filename, measurements=20, sep=1):
#     calibrate_results = {}
#     for label in LABELS:
#         calibrate_results[label] = [[], []]

#     for _ in range(sep):
#         for label in LABELS:
#             print('Please think {} for {} seconds'.format(label, measurements))
#             time.sleep(3)

#             # ik weet niet hoe we onze train data gaan opslaan, maar als we dat anders doen
#             # dan hier moeten we dit aanpassen
#             for _ in range(measurements):
#                 data = read_delete_when_available(filename)
#                 data = data.T
#                 c1 = data[0, 0:0.4*256]
#                 c2 = data[1, 0:0.6*256]
#                 result = analysis.analysis([c1], [c2])
#                 calibrate_results[label][0].append(result[0][0])
#                 calibrate_results[label][1].append(result[1][0])

#     return calibrate_results

# is gewoon een plot, niks meer aan doen
def show_calibration(calibration):
    analysis.plot(calibration)

# opslaan van de calibratie zodat het niet opnieuw hoeft te gebeuren
# def save_calibration(calibration, filename):
#     with open(filename, 'wb') as file:
#         pickle.dump(calibration, file)

# laden van calibratie
def load_calibration(filename):
    # with open(filename, 'rb') as csvfile:
    #     return pickle.load(file)
    # return np.genfromtxt('data.csv', delimiter=',')
    # return csv.reader(csvfile,delimiter=' ')
    return np.load('Klaas.npy',allow_pickle=True).T

# als er een calibratie file is dan wordt die geladen, anders wordt calibratie geinitieerd en opgeslagen
def init(args, filename='calibrations/data.csv'):
    if args.calibration_file:
        calibration = load_calibration(args.calibration_file)
        print("Sucessfully loaded {}".format(args.calibration_file))
    else:
        print('doe calibratie met -c Klaas.npy')
    # show_calibration(calibration)
    analysis.KNN = classify.create_knn_classifier(calibration)
    return calibration

# niks aan veranderen mits we het calibreren er in houden
if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='Live eeg classification demonstration')
        parser.add_argument('subject_name', help='The name of the measured subject.')
        parser.add_argument('-c', '--calibration_file',default=None, help='Load a calibration.')
        parser.add_argument('-d', '--drone', dest='drone', action='store_true', help='Use the drone.')
        args = parser.parse_args()
        # signal.signal(signal.SIGINT, handle_signint)

        DRONE = Drone()


        # anders dit weg doen
        calibration = init(args)
        print("Classifying each second")
        DRONE.takeoff()
        time.sleep(4)

        # VOEG DIT WEER TOE VOOR BEWEGEN
        DRONE.takeoff()
        periodically_classify(calibration, route_index, route_list) #
    except Exception as e:
        print(e)
        # handle_signint(1, 1)
