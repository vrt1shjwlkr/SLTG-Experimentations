import simpy, os, datetime, random, simplejson, urllib

googleAPIkey = "AIzaSyAYYBcuM_1R18E1Uwhk3Xz28zYJSc-x1ko"
#ubunt path
traceFolderPath = "/home/vshejwalkar/Dropbox/UMass/Amir H/Location Privacy/Synthetic Data Generation/Geolife Trajectories 1.3/sltgTF_exp1/"
class trace:
	def __init__(self, file_path, userID, locationsPath):
		self.file_path = file_path
		self.id = userID
		self.locations = {}
		self.trace = []
		self.total_distance = None
		self.speed = None
		self.displacement = None
		self.trace_spread = []
		self.markov_matrix = []
		self.location_prob = []

	def convertToTrace(self):
		with open(self.file_path, "r") as tf:
			for line in tf:
				self.trace.append(int(line.splitline(',')[-1]))
	
	def convertTolocations(self):
		with open(self.locations, "r") as lf:
			for i, line in enumerate(lf):
				self.locations[] = [float(line.splitline(',')[1]), float(line.splitline(',')[0])]
	
	def totalDistance(self):
		distance = 0
		for i in range(len(self.trace) - 1):
			source = self.locations[self.trace[i]]
			destination = self.locations[self.trace[i+1]]

			url = ("https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={0}&destinations={1}&key="+googleAPIkey).format(str(source),str(destination))
			result = simplejson.load(urllib.urlopen(url))
			intermediate_distance = ((result.get('rows')[0].get('elements')[0].get('distance').get('value')))
			self.trace_spread.append(intermediate_distance)
			distance += intermediate_distance

		self.totalDistance = distance
		self.speed = self.totalDistance/(len(self.trace))

		firstLoc = self.locations[self.trace[0]]
		lastLoc = self.locations[self.trace[-1]]
		url = ("https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={0}&destinations={1}&key="+googleAPIkey).format(str(source),str(destination))
		result = simplejson.load(urllib.urlopen(url))
		self.displacement += ((result.get('rows')[0].get('elements')[0].get('distance').get('value')))

	def calcMarkovMat(self):
