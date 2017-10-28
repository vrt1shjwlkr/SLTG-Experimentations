
def extractLocationData(datatDir, num_rows, num_cols):
	numOfUsers=0
	numExtraLocations=0

	for folderName in sorted(os.listdir(datatDir)):
		
		if folderName.startswith('.'):
			continue
		
		# Following folder contains traces of the user with ID - folderName
		traceDir=datatDir+'/'+folderName+'/trace'+folderName
		if not os.path.exists(traceDir):
			os.makedirs(traceDir)
		
		# Following folder contains LMP2 format traces to synthesize more traces
		lpmTraceDir=datatDir+'/'+folderName+'/lpmTrace'+folderName
		if not os.path.exists(lpmTraceDir):
			os.makedirs(lpmTraceDir)

		# Contains all the unique locations for the user
		uniqueLocation=[]

		# Number of files per user
		numOfFilesProcessed=0
		fileNum=1

		userLocationsFilePath=datatDir+"/"+folderName+"/user"+folderName+"Locations.dat" # All locations
		userLocationsFile=open(userLocationsFilePath,'w')

		# This folder has all the trajectories for user - folderName
		entryPath=datatDir+"/"+folderName+"/Trajectory/"

		# Each fileName file has one trajectory and we will sample it at 1/10 freq
		for fileName in sorted(os.listdir(entryPath)):
			tracePath=traceDir+'/trace'+str(fileNum)+'.trace'
			trace=open(tracePath,'w')

			lpmTracePath=lpmTraceDir+'/lpmTrace'+str(fileNum)+'.trace'
			lpmTrace=open(lpmTracePath,'w')

			filePath=os.path.join(entryPath, fileName)

			with open(filePath) as f:
				i=0
				for line in f:
					if(i>5 and (i%10==0)):
						params=line.rstrip().split(',')

						# Calculate the region based on lattitude and longitude
						lattitude = float(params[0])
						longitude = float(params[1])
						region_row = int(num_rows * (lattitude - 39.56)/(40.42-39.56))
						region_col = int(num_cols * (longitude - 115.68)/(117.15-115.68))
						region = num_rows * region_col + region_row

						if(region_col > 99 or region_row > 99):
							numExtraLocations+=1

						# Calculate timeslot based on exact time
						Time = datetime.datetime.strptime(params[6], '%H:%M:%S')
						timeSlot = int(12 * Time.time().hour + 0.2 * (Time.time().minute))
			
						string=str(folderName)+','+params[0]+','+params[1]+','+str(region)+','+params[6]+','+str(timeSlot)+'\n'
						userLocationsFile.write(string)
						trace.write(string)

						lpmString=folderName+','+str(region)+','+str(timeSlot)+'\n'
						lpmTrace.write(lpmString)					
					i+=1
			numOfFilesProcessed+=1
			fileNum+=1
		numOfUsers+=1
		if(numOfUsers >= 100):
			break