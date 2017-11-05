import matplotlib.pyplot as plt
import os

def plotDict(plotName, figName, ylabel, xlabel, dictionary, time):
	print "Number of line plots in data " + str(len(dictionary.keys()))
	f = plt.figure(figsize=(5,4))
	plt.title(plotName)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	for key, value in dictionary.iteritems():
		plt.plot(time, value, label = key)
	plt.axis([0,40,0,40])
	plt.legend(loc="upper right", prop={'size': 5})
	f.savefig(figName)

def plotFakes(plotsFolder):
	time = []
	realTrace = plotsFolder + 'input.trace'
	for i in range(1,41):
		time.append(i)
	# plotting fakes first
	for user in sorted(os.listdir(plotsFolder)):
		if user.startswith("user"):
			print "plotting fakes for " + user
			userData = {}
			userPlots = plotsFolder + user
			for trace in sorted(os.listdir(userPlots)):
				if ".info" not in trace and trace.startswith('synthetic'):
					traceName = trace.split('-')[-1]
					tracePath = userPlots + '/' + trace
					with open(tracePath, "r") as tf:
						for line in tf:
							if userData.has_key(traceName):
								userData[traceName].append(int(line.strip().split(',')[-1]))
							else:
								userData[traceName] = [int(line.strip().split(',')[-1])]
			with open(realTrace, 'r') as rtf:
				for line in rtf:
					if line.split(',')[0] == user[4:]:
						if userData.has_key("real trace"):
							userData["real trace"].append(int(line.split(',')[2]))
						else:
							userData["real trace"] = [int((line.split(',')[2]))]
			
			plotName = user + " synthetic traces"
			figName = plotsFolder + user[4:] + '_trace_plot.pdf'
			plotDict(plotName, figName, "location", "time", userData, time)

def plotPerConfig(configurationsFolder):
	for folder in sorted(os.listdir(plotsPath_exp12 + configurationsFolder)):
		print "plotting for configuration - " + configurationsFolder[6:] + " " + folder[4:]
		plotsPath = plotsPath_exp12 + configurationsFolder + folder + '/'
		plotFakes(plotsPath)

# mac
# plotsPath_exp11 = "/Users/Virat/Documents/Dropbox/UMass/Amir H/Location Privacy/Synthetic Data Generation/Geolife Trajectories 1.3/sltgTF_exp1/sltgTF_exp1.1/"
# plotsPath_exp12 = "/Users/Virat/Documents/Dropbox/UMass/Amir H/Location Privacy/Synthetic Data Generation/Geolife Trajectories 1.3/sltgTF_exp1/sltgTF_exp1.2/"
# ubuntu
plotsPath_exp12 = "/home/vshejwalkar/Dropbox/UMass/Amir H/Location Privacy/Synthetic Data Generation/Geolife Trajectories 1.3/sltgTF_exp1/sltgTF_exp1.2/"
plotsPath_exp11 = "/home/vshejwalkar/Dropbox/UMass/Amir H/Location Privacy/Synthetic Data Generation/Geolife Trajectories 1.3/sltgTF_exp1/sltgTF_exp1.1/"
# configurationsFolder = "fakes_5_84_225_250/"
configurationsFolder = "fakes_5_40_40_40.1/"
plotPerConfig(configurationsFolder)