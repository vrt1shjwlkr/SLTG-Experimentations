# given a seed and a fake trace calculate the generic utility of the 
# fake trace
import simpy, os, datetime, random, simplejson, urllib

def distance_bw_traces(seed, fake):
	for i in range (len(seed)):
		gen_distance += (distance_matrix[seed[i]][fake[i]])/len(seed)
	return gen_distance

def trace_distance(trace):
	for i in range(len(trace)):
		distance_covered += distance_matrix[trace[i]][trace[i+1]]