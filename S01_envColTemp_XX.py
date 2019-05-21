#!/usr/bin/env python
# -----------------------------------------------------------------------------
#  Reading temperature from ds18b20 and writing data to files
#    1 file = max 10 Mo; then new file
#    1 new file at each startup
#    data stored into the RAM every minute and writen to files every 10 minutes
#
#  (c) IRD / Francois Rebaudo, 2018
#  Affiliation: UMR EGCE ; IRD, CNRS, Univ. ParisSud, Univ. ParisSaclay ;
#    Gif-sur-Yvette, France
#
#  License: Creative Commons CC-BY-NC-SA
# -----------------------------------------------------------------------------

import glob
import time
import os
import csv

idLoc = "salleElevage_"
RAMReadNumber = 40
fileMaxSizeMo = 10

while True:
	currentTime = time.localtime()
	fNameYear = currentTime[0]
	fNameMonth = currentTime[1]
	if(fNameMonth < 10):
		fNameMonth = "0" + str(fNameMonth)
	fNameDay = currentTime[2]
	if(fNameDay < 10):
		fNameDay = "0" + str(fNameDay)
	fNameHour = currentTime[3]
	if(fNameHour < 10):
		fNameHour = "0" + str(fNameHour)
	fNameMin = currentTime[4]
	if(fNameMin < 10):
		fNameMin = "0" + str(fNameMin)
	fNameSec = currentTime[5]
	if(fNameSec < 10):
		fNameSec = "0" + str(fNameSec)
	fileName = idLoc + str(fNameYear) + str(fNameMonth) + str(fNameDay) + str(fNameHour) + str(fNameMin) + str(fNameSec)
	with open('%s.csv' % fileName, "w", newline = '') as myFile:
		myWriter = csv.writer(myFile, delimiter=';',
			quotechar='"', quoting=csv.QUOTE_MINIMAL)
		myWriter.writerow(["year","month","day","hour","minute","second","sensorId", "temperature"])
	fileSize = os.stat('%s.csv' % fileName).st_size * 9.54 * 10**(-7)

	while (fileSize < fileMaxSizeMo):
		sensorALL = []
		# adapted from Internet code under CC-BY-SA  ----------------------
		# see https://raspberrypi.stackexchange.com/questions/40378/ds18b20-address-finding
		while(len(sensorALL) < RAMReadNumber):
			if time.localtime()[5] == 0:
				for sensor in glob.glob("/sys/bus/w1/devices/28-00*/w1_slave"):
					id = sensor.split("/")[5]
					myTime = time.localtime()
					myTimeYear = myTime[0]
					myTimeMonth = myTime[1]
					myTimeDay = myTime[2]
					myTimeHour = myTime[3]
					myTimeMin = myTime[4]
					myTimeSec = myTime[5]
					try:
						f = open(sensor, "r")
						data = f.read()
						f.close()
						if "YES" in data:
							(discard, sep, reading) = data.partition(' t=')
							ds18b20t = float(reading) / 1000.0
						else:
							ds18b20t = 9999
						sensorX = [myTimeYear, myTimeMonth, myTimeDay, myTimeHour, myTimeMin, myTimeSec, id, ds18b20t]
						sensorALL.append(sensorX)
					except:
						pass
				time.sleep(2)
			# end of code adapted from Internet -------------------------------
		fileEnv = sensorALL
		# append data to file
		with open('%s.csv' % fileName, "a", newline = '') as myFile:
			myWriter = csv.writer(myFile, delimiter=';',
				quotechar='"', quoting=csv.QUOTE_MINIMAL)
			myWriter.writerows(fileEnv)
		# update fileSize
		fileSize = os.stat('%s.csv' % fileName).st_size * 9.54 * 10**(-7)
