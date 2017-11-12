# given an input.trace file return an array containing locations in all the seeds for each time instant.
from __future__ import division
import simpy, os, datetime, random, simplejson, urllib

# UbuntuPath
experiment1_files = '/home/vshejwalkar/Documents/Synthetic Data Generation/Geolife Trajectories 1.3/sltg_exp1/'
experiment2_files = '/home/vshejwalkar/Documents/Synthetic Data Generation/Geolife Trajectories 1.3/sltg_exp2/' 
experiment3_files = '/home/vshejwalkar/Documents/Synthetic Data Generation/Geolife Trajectories 1.3/sltg_exp3/'

def seed_locations_per_time(seeds, trace_len, num_of_users):
	locations_per_time = {}
	# locations_per_time = [[0 for i in range(num_of_users)] for j in range(trace_len)]
	for i in range(trace_len):
		locations_per_time[i] = []
	for i in range(num_of_users):
		for j in range(trace_len):
			locations_per_time[j].append(seeds[i][j])
	return locations_per_time

def surge_factor(trace, trace_len, locations_per_time, num_of_users):
	surge = 0
	for i in range(trace_len):
		surge += (locations_per_time[i].count(trace[i]))/num_of_users
		surge = round(surge, 3)
	return surge

# locations_per_time = seed_locations_per_time(input_trace_file, 40, 5)
# print locations_per_time