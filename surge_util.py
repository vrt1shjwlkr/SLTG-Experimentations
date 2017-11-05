# given an input.trace file return an array containing locations in all
# the seeds for each time instant.
import simpy, os, datetime, random, simplejson, urllib

# MacPath
input_trace_file = '/Users/Virat/Documents/UMass Code/Synthetic Data Generation/Geolife Trajectories 1.3/sltgTF_exp1/sltgTF_exp1.2/fakes_5_40_40_40/out1_0_0_1_20/input.trace'

def seed_locations_per_time(input_trace_file, trace_len, num_of_users):
	locations_per_time = [[0 for i in range(num_of_users)] for j in range(trace_len)]

	with open(input_trace_file, 'r') as tf:
		for i, line in enumerate(tf, 0):
			locations_per_time[ (i%trace_len) ][ int(line.split(',')[0]) - 1 ] = int( line.split(',')[-1] )

	return locations_per_time

def surge_factor(trace, trace_len, locations_per_time, num_of_users):
	for i in range(trace_len):
		surge += (locations_per_time[i].count(trace[i]))/num_of_users

# locations_per_time = seed_locations_per_time(input_trace_file, 40, 5)
# print locations_per_time