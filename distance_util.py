# given a seed and a fake trace calculate the generic utility of the 
# fake trace
from __future__ import division
import simpy, os, datetime, random, simplejson, urllib, csv
from surge_util import *

# UbuntuPath
experiment1_files = '/home/vshejwalkar/Documents/Synthetic Data Generation/Geolife Trajectories 1.3/sltg_exp1/'
experiment2_files = '/home/vshejwalkar/Documents/Synthetic Data Generation/Geolife Trajectories 1.3/sltg_exp2/' 
experiment3_files = '/home/vshejwalkar/Documents/Synthetic Data Generation/Geolife Trajectories 1.3/sltg_exp3/'

distance_matrix = [[0, 743, 6344, 6281, 6237, 6486, 5558, 4254, 3100, 1940, 2438, 2523, 2445, 2444, 2087, 2334, 3742, 6079, 5909, 6284, 6265, 5630, 5787, 6361, 6060, 4931, 3308, 2054, 96, 2445, 2258, 2214, 3338, 5675, 5701, 5669, 3609, 2174, 216, 2444], [743, 0, 6061, 5998, 5954, 6203, 5275, 3971, 2817, 1178, 1676, 1761, 1683, 1682, 1325, 1572, 3459, 5796, 5627, 6001, 5983, 5347, 5505, 6078, 5778, 4648, 2546, 1292, 840, 1682, 1496, 1452, 3056, 5392, 5419, 5386, 3327, 1412, 528, 1682], [6344, 6061, 0, 267, 446, 840, 1533, 3504, 4092, 5257, 4997, 4959, 5057, 5055, 5403, 4328, 3628, 3036, 1285, 638, 639, 992, 1871, 2330, 1886, 3880, 3975, 5371, 10022, 5056, 5575, 4294, 3784, 1181, 1052, 3218, 3912, 4212, 9710, 5055], [6281, 5998, 267, 0, 383, 777, 1470, 3441, 3949, 5114, 4855, 4816, 4914, 4913, 5261, 4186, 3486, 2972, 1222, 575, 576, 849, 1728, 2187, 1743, 3737, 3832, 5228, 9879, 4913, 5432, 4151, 3641, 1118, 988, 3155, 3769, 4069, 9567, 4913], [6237, 5954, 446, 383, 0, 355, 1171, 3176, 4287, 5452, 5193, 5154, 5252, 5250, 5599, 4524, 3824, 2661, 924, 234, 234, 1005, 1883, 2342, 1899, 4075, 4170, 5566, 10217, 5251, 5770, 4489, 3979, 820, 945, 2844, 4107, 4407, 9905, 5250], [6486, 6203, 840, 777, 355, 0, 1255, 3260, 4370, 5535, 5276, 5237, 5335, 5334, 5682, 4607, 3907, 2744, 1007, 317, 318, 1234, 2113, 2572, 2128, 4158, 4253, 5649, 10300, 5334, 5853, 4572, 4062, 903, 1175, 2927, 4190, 4490, 9988, 5334], [5558, 5275, 1533, 1470, 1171, 1255, 0, 2206, 3950, 5114, 4855, 4817, 4914, 4913, 5261, 4186, 2684, 1690, 586, 1050, 1051, 1936, 2409, 2978, 2678, 3737, 3832, 5228, 9879, 4914, 5432, 4151, 3641, 352, 1668, 1873, 2921, 4070, 9567, 4913], [4254, 3971, 3504, 3441, 3176, 3260, 2206, 0, 1347, 2749, 3011, 2973, 3254, 3252, 2896, 2342, 512, 1321, 2514, 2973, 2978, 3230, 3387, 3960, 3660, 2885, 2007, 2863, 4520, 3253, 3067, 2307, 1030, 2279, 3596, 564, 778, 2226, 4208, 3252], [3100, 2817, 4092, 3949, 4287, 4370, 3950, 1347, 0, 1497, 1995, 2080, 2002, 2000, 1644, 1891, 776, 2428, 3099, 3563, 3564, 3443, 3600, 4173, 3873, 2748, 1870, 1611, 3268, 2001, 1815, 1771, 404, 2865, 3514, 1670, 493, 1731, 2956, 2000], [1940, 1178, 5257, 5114, 5452, 5535, 5114, 2749, 1497, 0, 614, 576, 673, 672, 585, 707, 2803, 5140, 4971, 5345, 5327, 4691, 4849, 5422, 5122, 3992, 1361, 553, 2918, 673, 706, 588, 2400, 4736, 4763, 4730, 2671, 547, 2607, 672], [2438, 1676, 4997, 4855, 5193, 5276, 4855, 3011, 1995, 614, 0, 48, 59, 58, 351, 1324, 2521, 5635, 4688, 5062, 5044, 4409, 4566, 5139, 4839, 3016, 1049, 404, 3413, 59, 281, 1205, 2117, 4454, 4480, 3432, 2388, 1165, 3101, 58], [2523, 1761, 4959, 4816, 5154, 5237, 4817, 2973, 2080, 576, 48, 0, 124, 125, 399, 1286, 2482, 5719, 4650, 5024, 5006, 4370, 4528, 5101, 4801, 2978, 1011, 453, 3497, 124, 329, 1167, 2079, 4415, 4442, 3394, 2350, 1126, 3185, 125], [2445, 1683, 5057, 4914, 5252, 5335, 4914, 3254, 2002, 673, 59, 124, 0, 1, 358, 1383, 2580, 5642, 4747, 5122, 5103, 4468, 4625, 5199, 4898, 3075, 1108, 411, 3420, 0, 288, 1264, 2176, 4513, 4539, 3491, 2447, 1224, 3108, 1], [2444, 1682, 5055, 4913, 5250, 5334, 4913, 3252, 2000, 672, 58, 125, 1, 0, 357, 1382, 2579, 5640, 4746, 5120, 5102, 4467, 4624, 5197, 4897, 3074, 1107, 410, 3419, 1, 287, 1263, 2175, 4512, 4538, 3490, 2446, 1222, 3107, 0], [2087, 1325, 5403, 5261, 5599, 5682, 5261, 2896, 1644, 585, 351, 399, 358, 357, 0, 1013, 2947, 5283, 5114, 5488, 5470, 4835, 4992, 5565, 5265, 4136, 1400, 102, 3062, 358, 174, 894, 2543, 4880, 4906, 4874, 2814, 853, 2750, 357], [2334, 1572, 4328, 4186, 4524, 4607, 4186, 2342, 1891, 707, 1324, 1286, 1383, 1382, 1013, 0, 1852, 4278, 4019, 4393, 4375, 3740, 3897, 4470, 4170, 3041, 1174, 980, 3308, 1383, 1183, 119, 1448, 3785, 3811, 2763, 1719, 371, 2996, 1382], [3742, 3459, 3628, 3486, 3824, 3907, 2684, 512, 776, 2803, 2521, 2482, 2580, 2579, 2947, 1852, 0, 1669, 2361, 2825, 2826, 3067, 3225, 3798, 3498, 2373, 1495, 2382, 4039, 2558, 2586, 1795, 539, 2127, 3139, 911, 284, 1714, 3727, 2557], [6079, 5796, 3036, 2972, 2661, 2744, 1690, 1321, 2428, 5140, 5635, 5719, 5642, 5640, 5283, 4278, 1669, 0, 1818, 2282, 2282, 2549, 2707, 3280, 2979, 2441, 2492, 3888, 5545, 3573, 4092, 2811, 1719, 1583, 2621, 290, 1468, 2729, 5233, 3572], [5909, 5627, 1285, 1222, 924, 1007, 586, 2514, 3099, 4971, 4688, 4650, 4747, 4746, 5114, 4019, 2361, 1818, 0, 1664, 1646, 1665, 1823, 2392, 2092, 3151, 3246, 4642, 9293, 4328, 4846, 3565, 3055, 1074, 1082, 2859, 3184, 3484, 8981, 4327], [6284, 6001, 638, 575, 234, 317, 1050, 2973, 3563, 5345, 5062, 5024, 5122, 5120, 5488, 4393, 2825, 2282, 1664, 0, 115, 1032, 1911, 2370, 1926, 3956, 4051, 5447, 10098, 5132, 5651, 4370, 3860, 701, 972, 2621, 3988, 4288, 9786, 5131], [6265, 5983, 639, 576, 234, 318, 1051, 2978, 3564, 5327, 5044, 5006, 5103, 5102, 5470, 4375, 2826, 2282, 1646, 115, 0, 1211, 2090, 3081, 2105, 3841, 3935, 5332, 9982, 5017, 5535, 4254, 3744, 585, 882, 2609, 3873, 4173, 9671, 5016], [5630, 5347, 992, 849, 1005, 1234, 1936, 3230, 3443, 4691, 4409, 4370, 4468, 4467, 4835, 3740, 3067, 2549, 1665, 1032, 1211, 0, 1279, 1738, 1294, 3288, 3382, 4779, 9429, 4464, 4982, 3701, 3192, 1576, 1446, 2995, 3320, 3620, 9118, 4463], [5787, 5505, 1871, 1728, 1883, 2113, 2409, 3387, 3600, 4849, 4566, 4528, 4625, 4624, 4992, 3897, 3225, 2707, 1823, 1911, 2090, 1279, 0, 551, 1130, 2686, 3890, 5208, 8850, 4829, 5411, 4130, 3620, 2293, 2163, 3424, 3749, 4049, 8538, 4828], [6361, 6078, 2330, 2187, 2342, 2572, 2978, 3960, 4173, 5422, 5139, 5101, 5199, 5197, 5565, 4470, 3798, 3280, 2392, 2370, 3081, 1738, 551, 0, 1020, 2133, 3337, 5448, 8297, 4276, 5651, 4370, 3684, 2541, 2411, 3664, 3857, 4289, 7985, 4275], [6060, 5778, 1886, 1743, 1899, 2128, 2678, 3660, 3873, 5122, 4839, 4801, 4898, 4897, 5265, 4170, 3498, 2979, 2092, 1926, 2105, 1294, 1130, 1020, 0, 2282, 3486, 5183, 8446, 4869, 5387, 4106, 3596, 2276, 2146, 3400, 3725, 4025, 8134, 4868], [4931, 4648, 3880, 3737, 4075, 4158, 3737, 2885, 2748, 3992, 3016, 2978, 3075, 3074, 4136, 3041, 2373, 2441, 3151, 3956, 3841, 3288, 2686, 2133, 2282, 0, 2336, 4159, 8189, 3275, 4363, 3082, 2683, 2614, 2641, 2393, 2856, 3000, 7877, 3274], [3308, 2546, 3975, 3832, 4170, 4253, 3832, 2007, 1870, 1361, 1049, 1011, 1108, 1107, 1400, 1174, 1495, 2492, 3246, 4051, 3935, 3382, 3890, 3337, 3486, 2336, 0, 1453, 4339, 1108, 1330, 1218, 1641, 3428, 3455, 2407, 1913, 1060, 4027, 1107], [2054, 1292, 5371, 5228, 5566, 5649, 5228, 2863, 1611, 553, 404, 453, 411, 410, 102, 980, 2382, 3888, 4642, 5447, 5332, 4779, 5208, 5448, 5183, 4159, 1453, 0, 3029, 411, 181, 861, 2510, 4847, 4874, 4841, 2782, 821, 2717, 410], [96, 840, 10022, 9879, 10217, 10300, 9879, 4520, 3268, 2918, 3413, 3497, 3420, 3419, 3062, 3308, 4039, 5545, 9293, 10098, 9982, 9429, 8850, 8297, 8446, 8189, 4339, 3029, 0, 2541, 2354, 2311, 3434, 5771, 5798, 5765, 3705, 2270, 312, 2540], [2445, 1682, 5056, 4913, 5251, 5334, 4914, 3253, 2001, 673, 59, 124, 0, 1, 358, 1383, 2558, 3573, 4328, 5132, 5017, 4464, 4829, 4276, 4869, 3275, 1108, 411, 2541, 0, 287, 1264, 2176, 4512, 4539, 3491, 2447, 1223, 3108, 1], [2258, 1496, 5575, 5432, 5770, 5853, 5432, 3067, 1815, 706, 281, 329, 288, 287, 174, 1183, 2586, 4092, 4846, 5651, 5535, 4982, 5411, 5651, 5387, 4363, 1330, 181, 2354, 287, 0, 1015, 2664, 5001, 5028, 4995, 2935, 974, 2871, 287], [2214, 1452, 4294, 4151, 4489, 4572, 4151, 2307, 1771, 588, 1205, 1167, 1264, 1263, 894, 119, 1795, 2811, 3565, 4370, 4254, 3701, 4130, 4370, 4106, 3082, 1218, 861, 2311, 1264, 1015, 0, 1413, 3750, 3776, 2728, 1684, 340, 2877, 1263], [3338, 3056, 3784, 3641, 3979, 4062, 3641, 1030, 404, 2400, 2117, 2079, 2176, 2175, 2543, 1448, 539, 1719, 3055, 3860, 3744, 3192, 3620, 3684, 3596, 2683, 1641, 2510, 3434, 2176, 2664, 1413, 0, 2564, 3250, 1429, 251, 1679, 3194, 2239], [5675, 5392, 1181, 1118, 820, 903, 352, 2279, 2865, 4736, 4454, 4415, 4513, 4512, 4880, 3785, 2127, 1583, 1074, 701, 585, 1576, 2293, 2541, 2276, 2614, 3428, 4847, 5771, 4512, 5001, 3750, 2564, 0, 1317, 1990, 3418, 3718, 9216, 4561], [5701, 5419, 1052, 988, 945, 1175, 1668, 3596, 3514, 4763, 4480, 4442, 4539, 4538, 4906, 3811, 3139, 2621, 1082, 972, 882, 1446, 2163, 2411, 2146, 2641, 3455, 4874, 5798, 4539, 5028, 3776, 3250, 1317, 0, 2167, 3417, 3717, 9215, 4560], [5669, 5386, 3218, 3155, 2844, 2927, 1873, 564, 1670, 4730, 3432, 3394, 3491, 3490, 4874, 2763, 911, 290, 2859, 2621, 2609, 2995, 3424, 3664, 3400, 2393, 2407, 4841, 5765, 3491, 4995, 2728, 1429, 1990, 2167, 0, 1178, 2975, 4647, 3818], [3609, 3327, 3912, 3769, 4107, 4190, 2921, 778, 493, 2671, 2388, 2350, 2447, 2446, 2814, 1719, 284, 1468, 3184, 3988, 3873, 3320, 3749, 3857, 3725, 2856, 1913, 2782, 3705, 2447, 2935, 1684, 251, 3418, 3417, 1178, 0, 1808, 3430, 2474], [2174, 1412, 4212, 4069, 4407, 4490, 4070, 2226, 1731, 547, 1165, 1126, 1224, 1222, 853, 371, 1714, 2729, 3484, 4288, 4173, 3620, 4049, 4289, 4025, 3000, 1060, 821, 2270, 1223, 974, 340, 1679, 3718, 3717, 2975, 1808, 0, 2836, 1222], [216, 528, 9710, 9567, 9905, 9988, 9567, 4208, 2956, 2607, 3101, 3185, 3108, 3107, 2750, 2996, 3727, 5233, 8981, 9786, 9671, 9118, 8538, 7985, 8134, 7877, 4027, 2717, 312, 3108, 2871, 2877, 3194, 9216, 9215, 4647, 3430, 2836, 0, 2228], [2444, 1682, 5055, 4913, 5250, 5334, 4913, 3252, 2000, 672, 58, 125, 1, 0, 357, 1382, 2557, 3572, 4327, 5131, 5016, 4463, 4828, 4275, 4868, 3274, 1107, 410, 2540, 1, 287, 1263, 2239, 4561, 4560, 3818, 2474, 1222, 2228, 0]]

def distance_bw_traces(seed, fake):
	gen_distance = 0
	for i in range (len(seed)):
		gen_distance += (distance_matrix[seed[i]-1][fake[i]-1])/len(seed)
		gen_distance = round(gen_distance, 3)
	return gen_distance

def trace_distance(fake):
	distance_covered = 0
	for i in range(len(fake)-1):
		distance_covered += distance_matrix[fake[i]-1][fake[i+1]-1]
	return distance_covered

def get_fakes(experiment_path, files_path, folder_name):
	seeds = []
	fakes = {}
	
	for file_name in sorted(os.listdir(experiment_path + files_path + '/' + folder_name + '/')):
		if file_name == 'input.trace':
			# print 'extracting seed for configuration {}'.format(row_to_csv)
			seeds = get_seeds(experiment_path + files_path + '/' + folder_name + '/input.trace', files_path.split('_')[1], files_path.split('_')[2])
		if file_name == 'out':
			for user_data in sorted(os.listdir(experiment_path + files_path + '/' + folder_name + '/out/')):
				user_fakes = []
				# print 'extracting fakes of user {}'.format(int(user_data[4:]))
				for fake in sorted(os.listdir(experiment_path + files_path + '/' + folder_name + '/out/' + user_data + '/')):
					if not fake.endswith('.info'):
						fake_trace =[]
						with open((experiment_path + files_path + '/' + folder_name + '/out/' + user_data + '/' + fake), 'r') as ft:
							for line in ft:
								fake_trace.append(int(line.split(',')[-1]))
						user_fakes.append(fake_trace)
				fakes[int(user_data[4:])] = user_fakes
	return seeds, fakes


def get_seeds(input_trace, num_of_users, num_timestamps):
	with open(input_trace, 'r') as tf:
		user_seed = []
		seed = []
		j = 0
		for time_stamp, line in enumerate(tf, 1):
			user_seed.append(int(line.split(',')[-1]))
			if time_stamp % int(num_timestamps) == 0:
				# print 'adding seed of user {}'.format(j+1)
				seed.append(user_seed)
				j += 1
				user_seed = []
		return seed

def calculate_metrics():
	with open('results.csv', 'w') as rf:
		rf_writer = csv.writer(rf)
		header = ['experiment', 'num of users', 'trace length', 'max location in trace', 'max location allowed', 'Clusters', 'GLRP', 'MP', 'ALRP', 'VF', 'User', 'fake trace num','Generic Util', 'Seed distance', 'Trace distance', 'Surge factor']
		rf_writer.writerow(header)
		for folder in sorted(os.listdir(experiment1_files)):
			print folder
			config = folder.split('_')
			for config_path in sorted(os.listdir(experiment1_files + folder + '/')):
				seeds = []
				fakes = {}
				if config_path.startswith('out_'):
					# exp_num, num_of_users, num_timestamps, num_locations_in_trace, num_allowed_locations
					row_to_csv = []
					row_to_csv = [experiment1_files.split('/')[-2], config[1], config[2], config[3], config[4], config[5]]
					row_to_csv.append(config_path.split('_')[1]) # GLRP				
					row_to_csv.append(config_path.split('_')[2]) # MP
					row_to_csv.append(config_path.split('_')[3]) # ALRP
					row_to_csv.append(config_path.split('_')[4]) # Viterbi factor
					seeds,fakes = get_fakes(experiment1_files, folder, config_path)

					locations_per_time = seed_locations_per_time(seeds, int(config[2]), int(config[1]))

					for i in range(len(seeds)):
						print 'calculating metrics for configurate {} user {}'.format(row_to_csv, i+1)
						seed = seeds[i]
						seed_distance_covered = trace_distance(seed)
						# fetching fakes
						for j in range(len(fakes.get(i+1))):
							fake = fakes.get(i+1)[j]
							gen_distance = distance_bw_traces(seed, fake)
							distance_covered = trace_distance(fake)
							surge = surge_factor(fake, int(config[2]), locations_per_time, int(config[1]))
							row_to_csv.append(i+1)
							row_to_csv.append(j)
							row_to_csv.append(gen_distance)
							row_to_csv.append(seed_distance_covered)
							row_to_csv.append(distance_covered)
							row_to_csv.append(surge)
							rf_writer.writerow(row_to_csv)
							row_to_csv = row_to_csv[:-6]
		# break

calculate_metrics()