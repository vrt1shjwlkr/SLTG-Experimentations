########################################################################################
#	The script will extract unique locations for each user in the geolocation data.    #
#	Unique locations are saved in userXXXLocations.txt; XXX is userID                  #
#                                                                                      #
#                                                                                      #
#                                                                                      #
########################################################################################
import os, glob, math
import datetime
import os, random
import xlrd, xlwt
from xlutils.copy import copy
from decimal import *
#for Ubuntu
datatDir = "/home/vshejwalkar/Documents/Location Data/GoeMesa Data/Geolife Trajectories 1.3/Data"
fakeTracesPath = "/home/vshejwalkar/Dropbox/UMass/Amir H/Location Privacy/Synthetic Data Generation/sglt-v0.1a/sg-LPM/build/out/"
#for MacBook
# datatDir = "/Users/Virat/Documents/Dropbox/UMass/Amir H/Location Privacy/Synthetic Data Generation/Geolife Trajectories 1.3/Data"

regionLon1=116.2
regionLon2=116.4
regionLat1=39.1
regionLat2=40.1

def locationTraceGenerator(datatDir):
	global regionLon1, regionLon2, regionLat1, regionLat2
	validUsers = []
	uniqueLocations = {}
	locationData = {}
	userID = 1
	locationsFile = "locations"
	lf = open(locationsFile, "w")
	traceFilePath = "input.trace"
	tf = open(traceFilePath, "w")

	for folderName in sorted(os.listdir(datatDir)):
		# Following time and location are timeslot and region for input.trace file of SLTG tool - userID,time,location
		time = 1
		print folderName
		if folderName.startswith('.') or folderName.startswith('000'):
			continue		
		# This folder has all the trajectories for user - folderName
		entryPath = datatDir+"/"+folderName+"/Trajectory/"
		string = ''
		string_trace = ''
		userDataPoints = 0
		# Each fileName file has one trajectory and we will sample it at 1/10 freq
		for fileName in sorted(os.listdir(entryPath)):
			filePath = os.path.join(entryPath, fileName)
			with open(filePath) as f:
				i = 0
				timeSeconds = -1
				location = []
				for line in f:
					if(i < 6):
						i+=1
						continue

					params = line.rstrip().split(',')
					# Calculate timeslot based on exact time
					Time = datetime.datetime.strptime(params[6], '%H:%M:%S')
					timeSecondsNew = Time.time().hour * 3600 + Time.time().minute * 60 + Time.time().second
					if timeSeconds == -1:
						timeSeconds = timeSecondsNew
					if not location:
						location = [params[1], params[0]]
						if locationData.has_key(userID):
							if locationData[userID].has_key(timeSecondsNew):
								locationData[userID][timeSecondsNew].append(location)
							else:
								locationData[userID][timeSecondsNew] = [location]
						else:
							locationData[userID] = {timeSecondsNew: location}

					# Location tuple is valid only if separated by 5min duration
					if timeSecondsNew > (timeSeconds + 300):
						location = [params[1], params[0]] # longitude, lattitude
						if locationData.has_key(userID):
							if locationData[userID].has_key(timeSecondsNew):
								locationData[userID][timeSecondsNew].append(location)
							else:
								locationData[userID][timeSecondsNew] = [location]
						else:
							locationData[userID] = {timeSecondsNew: location}

						if location not in uniqueLocations.values():
							uniqueLocations[len(uniqueLocations) + 1] = location
							string += (str(params[1]) + ',' + str(params[0]) + '\n')
							string_trace += (str(userID)+','+str(time)+','+str(len(uniqueLocations))+'\n')
							time += 1
						timeSeconds = timeSecondsNew
						userDataPoints += 1
					i += 1
					if userDataPoints >= 168:
						break
			if userDataPoints >= 168:
				lf.write(string)
				tf.write(string_trace)
				break

		if userDataPoints >= 168:
			validUsers.append(userID)
			userID += 1
		else:
			print "less than 200 datapoints - skipping user ", folderName
			locationData.pop(userID)
		if len(validUsers) == 5:
			break

def inputMobility(numUniqueLocations):
	mobility = "input.mobility"
	lf = open(mobility, "w")
	
	for i in range(numUniqueLocations):
		string = ''
		for j in range(numUniqueLocations - 1):
			# print i, j
			string += str(random.randint(0,1)) + ','
		string += str(random.randint(0,1))+'\n'
		lf.write(string)

def extractLPMData(datatDir, regions):	
	locationData = xlwt.Workbook()
	lon = locationData.add_sheet("Longitude")
	lat = locationData.add_sheet("Latitude")
	tim = locationData.add_sheet("Time")
	utl = locationData.add_sheet("user-time-location")
	
	numOfUsers = 0
	validUsers = []
	column = 0
	sltgData = {}
	userID = 1
	for folderName in sorted(os.listdir(datatDir)):
		print folderName
		if folderName.startswith('.'):
			continue

		# Number of files per user
		numOfFilesProcessed = 0
		row_num = 0
		# Lists to store data
		latitude = []
		longitude = []
		time = []
		
		# This folder has all the trajectories for user - folderName
		entryPath = datatDir+"/"+folderName+"/Trajectory/"

		# Each fileName file has one trajectory and we will sample it at 1/10 freq
		for fileName in sorted(os.listdir(entryPath)):
			filePath = os.path.join(entryPath, fileName)

			with open(filePath) as f:
				i = 0
				timeSeconds = -1
				timeSlot = -1
				region = -1
				for line in f:
					if(i < 6):
						i+=1
						continue

					params = line.rstrip().split(',')

					# Calculate timeslot based on exact time
					Time = datetime.datetime.strptime(params[6], '%H:%M:%S')
					timeSecondsNew = Time.time().hour * 3600 + Time.time().minute * 60 + Time.time().second
					timeSlotNew = int(12 * Time.time().hour + 0.2 * (Time.time().minute))

					if timeSeconds == -1:
						timeSeconds = timeSecondsNew
					if timeSlot == -1:
						timeSlot = timeSlotNew
					if region == -1:
						region_row = int(regions * ((float(params[1]) - regionLon1)/(regionLon2-regionLon1)))
						region_col = int(regions * ((float(params[0]) - regionLat1)/(regionLat2-regionLat1)))
						region = (regions * region_col) + region_row + 1
						if region >= 1 and region <= regions**2:
							if sltgData.has_key(userID):
								if sltgData[userID].has_key(timeSlotNew):
									sltgData[userID][timeSlotNew].append(region)
								else:
									sltgData[userID][timeSlotNew] = [region]
							else:
								sltgData[userID] = {timeSlotNew : [region]}
						# else:
						# 	print params[0], params[1], region, region_col, region_row
					
					# Location tuple is valid only if separated by 5min duration
					if timeSecondsNew > (timeSeconds + 300):
						timeSlotNew = int(12 * Time.time().hour + 0.2 * (Time.time().minute))
						
						latitude.append(float(params[0]))
						longitude.append(float(params[1]))
						time.append(params[6])

						region_row = int(regions * ((float(params[1]) - regionLon1)/(regionLon2-regionLon1)))
						region_col = int(regions * ((float(params[0]) - regionLat1)/(regionLat2-regionLat1)))
						region = (regions * region_col) + region_row + 1
						# print region_row, region_col, region
						if region >= 1 and region <= regions**2:
							if sltgData.has_key(userID):
								if sltgData[userID].has_key(timeSlotNew):
									sltgData[userID][timeSlotNew].append(region)
								else:
									sltgData[userID][timeSlotNew] = [region]
							else:
								sltgData[userID] = {timeSlotNew : [region]}

						timeSeconds = timeSecondsNew
						row_num += 1
					i += 1
			numOfFilesProcessed += 1
		if(row_num > 1000):
			lon.write(0, column, int(folderName))
			lat.write(0, column, int(folderName))
			tim.write(0, column, int(folderName))

			for j in range(1, len(latitude)):
				lon.write(j, column, longitude[j])
				lat.write(j, column, latitude[j])
				tim.write(j, column, time[j])
			column += 1
			validUsers.append(userID)
			userID += 1
		else:
			print "less than 1000 datapoints - skipping user ", folderName
			sltgData.pop(userID)
		numOfUsers += 1
		if len(validUsers) == 5:
			break
	locationData.save("locationData.xls")
	
	# ubuntu paths
	tfExp11 = "/home/vshejwalkar/Dropbox/UMass/Amir H/Location Privacy/Synthetic Data Generation/Geolife Trajectories 1.3/sltgTF_exp1/sltgTF_exp1.1/"
	tfExp12 = "/home/vshejwalkar/Dropbox/UMass/Amir H/Location Privacy/Synthetic Data Generation/Geolife Trajectories 1.3/sltgTF_exp1/sltgTF_exp1.2/"
	# mac Paths
	# tfExp11 = "/Users/Virat/Documents/Dropbox/UMass/Amir H/Location Privacy/Synthetic Data Generation/Geolife Trajectories 1.3/sltgTF_exp1/sltgTF_exp1.1/"
	# tfExp12 = "/Users/Virat/Documents/Dropbox/UMass/Amir H/Location Privacy/Synthetic Data Generation/Geolife Trajectories 1.3/sltgTF_exp1/sltgTF_exp1.2/"
	createTraces(sltgData, validUsers, regions, tfExp11) 


def createTraces(sltgData, validUsers, regions, traceFolderPath):

	print "Number of users in the trace data {}".format(len(sltgData))
	
	if not os.path.exists(traceFolderPath):
		os.makedirs(traceFolderPath)
	transCountMatrix = {}
	
	traceFilePath = traceFolderPath + "input.trace"
	tf = open(traceFilePath, "w")
	for key, value in sltgData.iteritems():
		if key in validUsers:
			print "Creating traces for userID: " + str(key)

			minTimeStamp = sltgData[key].keys()[0]
			maxTimeStamp = sltgData[key].keys()[-1]
			trace = []
			startTime = random.randint(minTimeStamp, (maxTimeStamp - 84))
			p = 1
			for i in range(startTime, startTime + 84):
				if value.has_key(i):
					loc = random.choice(value[i])
					string = str(key)+","+str(p)+","+str(loc) + "\n"
					trace.append(loc)
					tf.write(string)
					p += 1
				else:
					j = 1
					while value.has_key(i-j) == False:
						j += 1
					loc = random.choice(value[i-j])
					string = str(key)+","+str(p)+","+str(loc) + "\n"
					trace.append(loc)
					tf.write(string)
					p += 1

			# userTransMatrix = transCount(key, trace, regions)
			# transCountMatrix[key] = userTransMatrix

def transCount(userID, userTrace, regions):
	w, h = regions**2, regions**2
	transCountMatrix = [[0 for x in range(w)] for y in range(h)]
	print "Calculating transition matrices for real trace of user " + str(userID)
	normFactor = len(userTrace)-1 

	for i in range(normFactor):
		transProb = Decimal(1)/Decimal(normFactor)
		transCountMatrix[userTrace[i]-1][userTrace[i+1]-1] += round(transProb,4)
	return transCountMatrix

def fakeTracesTransMatrix(fakesPath):
	fakeTransitionMatrix = {}
	for folderName in sorted(os.listdir(fakesPath)):
		if folderName.startswith('.'):
			continue

		print "Calculating transitions count matrix for " + folderName
		
		userTransMatrix = {}
		entryPath = fakesPath + folderName + "/"

		for fileName in sorted(os.listdir(entryPath)):
			if fileName.endswith('.info'):
				continue			
			print "Converting trace file " + fileName + " to trace list"
			transtions = []
			filePath = os.path.join(entryPath, fileName)
			with open(filePath) as tf:
				for line in tf:
					transtions.append(int(line.split(',')[-1]))
			
			fakeTransMat = transCount(folderName, transtions)
			userTransMatrix[int(fileName.split('-')[-1][5:])] = fakeTransMat
	
		fakeTransitionMatrix[int(folderName[4:])] = userTransMatrix
	print fakeTransitionMatrix

def fakeSeedGen(datatDir):
	userID = 1
	totalLoc = 250
	
extractLPMData(datatDir, 15)
# locationTraceGenerator(datatDir)
# inputMobility(250)