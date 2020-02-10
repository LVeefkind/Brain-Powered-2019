import numpy as np
from itertools import groupby
from operator import itemgetter


#main function that gets the desired dios from the data
def get_dio(dio_channels):
	dio_dict = dict.fromkeys([0,1,2]) #initialize dict for the dios

	#find all non zero values for the dios
	dio_1_index = np.where(dio_channels[0] != 0)[0]
	dio_2_index = np.where(dio_channels[1] != 0)[0]
	dio_3_index = np.where(dio_channels[2] != 0)[0]
	dio_4_index = np.where(dio_channels[3] != 0)[0]

	#dio_5_index = np.where(dio_channels[4] != 0)[0]
	#dio_6_index = np.where(dio_channels[5] != 0)[0]

	#channel 7 = channel 1+2 and 8 = 1+3
	#3filter_1_7 = list(set(dio_1_index) & set(dio_2_index))
	#filter_1_8 = list(set(dio_1_index) & set(dio_3_index))

	#filter_for_dio_1 = filter_1_7+filter_1_8

	#add all the dio index where they are nonzero to the dict, with filtering the noise
	#dio_dict[0] = remove_noise(ranges(list(set(dio_1_index)-set(filter_for_dio_1))))
	#dio_dict[1] = remove_noise(ranges(list(set(dio_2_index)-set(dio_1_index))))
	#dio_dict[2] = remove_noise(ranges(list(set(dio_3_index)-set(dio_1_index))))



	dio_dict[0] = remove_noise(ranges(dio_1_index))
	dio_dict[1] = remove_noise(ranges(dio_2_index))
	dio_dict[2] = remove_noise(ranges(dio_3_index))
	dio_dict[3] = remove_noise(ranges(dio_4_index))
	#dio_dict[4] = remove_noise(ranges(dio_5_index))
	#dio_dict[5] = remove_noise(ranges(dio_6_index))
	#dio_dict[6] = remove_noise(ranges(filter_1_7))
	#dio_dict[7] = remove_noise(ranges(filter_1_8))

	return dio_dict

#function that gets the ranges of every dio
def ranges(nums):
    nums = sorted(set(nums))
    gaps = [[s, e] for s, e in zip(nums, nums[1:]) if s+1 < e]
    edges = iter(nums[:1] + sum(gaps, []) + nums[-1:])
    return list(zip(edges, edges))

#function that removes duplicates from a list
def remove_duplicates(x,y):
	x = x.tolist()
	for value in x:
		if value in y:
			x.remove(value)

	return x

#function that removes the noise from the dios.
def remove_noise(x):
	new_x = []
	for r in x:
		difference = r[1] - r[0]
		if 400 < difference < 600 :
			new_x.append(r)
	return new_x

