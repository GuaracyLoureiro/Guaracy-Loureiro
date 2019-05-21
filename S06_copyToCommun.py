#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#  Copy files located in Raspberry Pi "192.168.0.30" from the server 
# 
#  Francois Rebaudo and Romain Benoist, 2019
#  Affiliation: UMR EGCE ; IRD, CNRS, Univ. ParisSud, Univ. ParisSaclay ; 
#    Gif-sur-Yvette, France
# -----------------------------------------------------------------------------

import subprocess
import re # regexp -> grep

myId = 'salleElevage'
piFiles = {}
servFiles = {}

lsPi = subprocess.Popen(['ssh','-i','/home/bioinfo/.ssh/id_rsa','pi@192.168.0.30', 'ls', '-l', '/home/pi/Documents/'], stdout=subprocess.PIPE)
grepPi = subprocess.Popen(['grep', myId], stdin = lsPi.stdout, stdout=subprocess.PIPE)

for x in grepPi.stdout:
	fileSplit = str(x).split(' ')
	for y in fileSplit:
		findNum = re.findall('^[0-9]{5,9}(?![a-zA-Z])', y)
		if len(findNum) > 0:
			fileSize = findNum[0]
	fileName = fileSplit[-1].split('.')[0] + '.csv'
	piFiles[fileName] = fileSize


lsServ = subprocess.Popen(['ls', '-l', '/media/commun/Equipes/DEEIT/00_ELEVAGE/'], stdout=subprocess.PIPE)
grepServ = subprocess.Popen(['grep', myId], stdin = lsServ.stdout, stdout=subprocess.PIPE)


for x in grepServ.stdout:
	fileSplit = str(x).split(' ')
	for y in fileSplit:
		findNum = re.findall('^[0-9]{5,9}(?![a-zA-Z])', y)
		if len(findNum) > 0:
			fileSize = findNum[0]
	fileName = fileSplit[-1].split('.')[0] + '.csv'
	servFiles[fileName] = fileSize

print(piFiles)
print(servFiles)

downList = []
for k in piFiles:
	if k not in servFiles:
		print("File ", k, " downloaded")
		downList.append(k)
	if k in servFiles:
		if not piFiles[k] == servFiles[k]:
			print("File ", k, " updated")
			downList.append(k)

if len(downList) == 0:
	print("Everything up to date.")

for myFiles in downList:
	scp = subprocess.Popen(['scp','-i','/home/bioinfo/.ssh/id_rsa','pi@192.168.0.30:/home/pi/Documents/' + myFiles, '/media/commun/Equipes/DEEIT/00_ELEVAGE/'], stdout=subprocess.PIPE)
print("Done.")
