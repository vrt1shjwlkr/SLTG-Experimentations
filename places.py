# given a locations file, extract all the places near each of 
# the locations
import simpy, os, datetime, random, simplejson, urllib

location_file_path = '/Users/Virat/Documents/UMass Code/Synthetic Data Generation/Geolife Trajectories 1.3/sltgTF_exp1/sltgTF_exp1.2/fakes_5_40_40_40/out1_0_0_1_20/locations'
api_key = 'AIzaSyAYYBcuM_1R18E1Uwhk3Xz28zYJSc-x1ko'

def places(location_file_path, radius, search_type, keyword):
	places = []
	locations = []
	# create an array with all the locations
	with open(location_file_path, 'r') as lf:
		for line in lf:
			line_split = line.split(',')
			locations.append([float(line_split[0]), float(line_split[1])])
	
	places = [[] for i in range(len(locations))]

	for i in range(len(locations)):
		location = locations[i]
		lat = location[1]
		lon = location[0]
		url = 'https://maps.googleapis.com/maps/api/place/radarsearch/json?location={},{}&radius={}&type={}&keyword={}&key={}'.format(lat, lon, radius, search_type, keyword, api_key)
		print url, '\n'
		result = simplejson.load(urllib.urlopen(url))
		print result, '\n'
		for j in range(len(result.get('results'))):
			places[i].append(result.get('results')[j].get('place_id'))

	return places

places = places(location_file_path, 500, 'cafe', '')
# print places
