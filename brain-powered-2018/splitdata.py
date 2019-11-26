from collections import defaultdict
import diosplit
import numpy as np

"""
def split_data(dio_dict, data):
    pre_target_avg = np.zeros(shape=(6,6,256))
    target_avg = np.zeros(shape=(6,6,1024))

    # channels range from 1-8
    for channel in dio_dict:

        pre_target_list = [[],[],[],[],[],[]]
        target_list = [[],[],[],[],[],[]]

        # for every dio
        for dio in dio_dict[channel]:
            # find lower and upper boundaries of the DIO
            upper = dio[1]
            lower = dio[0]
            # add the requested indices from before/during/after the DIO to new
            # dictionaries
            #inplaats van 1 dio met 1 kanaal te linken, nu 1 dio met 8 kanalen
            for i in range(len(dio_dict)):
                #pre_cue_list[i].append(data[i][lower-pre_cue:lower])
                #cue_list[i].append(data[i][lower:lower+cue])
                pre_target_list[i].append(data[i][lower-256:lower])
                target_list[i].append(data[i][lower:lower+1024])
            pre_target_avg[channel] = np.average(np.array(pre_target_list), axis =1)
            target_avg[channel] = np.average(np.array(target_list), axis =1)


    return pre_target_avg, target_avg

"""
def split_data(dio_dict, data):

    target_list = [[],[],[],[],[],[],[]]
    # channels range from 1-8
    for channel in dio_dict:
        # for every dio
        for dio in dio_dict[channel]:
            # find lower and upper boundaries of the DIO
            upper = dio[1]
            lower = dio[0]
            # add the requested indices from before/during/after the DIO to new
            # dictionaries
            #inplaats van 1 dio met 1 kanaal te linken, nu 1 dio met 8 kanalen
            for i in range(len(target_list)-1):
                target_list[i].append(data[i][lower:lower+512])
            target_list[i+1].append(channel)

    return target_list