#!/usr/bin/Rscript
# -----------------------------------------------------------------------------
#  Reading temperature files and executing emailSender python script
#    if needed
#  
#  (c) IRD / Francois Rebaudo, 2018
#  Affiliation: UMR EGCE ; IRD, CNRS, Univ. ParisSud, Univ. ParisSaclay ; 
#    Gif-sur-Yvette, France
#  
#  License: Creative Commons CC-BY-NC-SA
# -----------------------------------------------------------------------------

setwd("/home/pi/Documents/")

#  parameters
# -----------------------------------------------------------------------------

files <- list.files(pattern = "^(.)*(csv)$")
files <- tail(files, n = 2)
paramMaxTemp <- c(31, #SNK_Kobodo_biberon_26
                  26, #Exterieur1
                  26, #SNF_cage_21
                  26, #SNK_Kobodo_cage_21
                  31, #SNK_Makindu_biberon_26
                  26, #Exterieur2
                  31, #SNF_biberon_26
                  26) #SNK_Makindu_cage_21
paramMinTemp <- c(21, #SNK_Kobodo_biberon_26
                  16, #Exterieur1
                  16, #SNF_cage_21
                  16, #SNK_Kobodo_cage_21
                  21, #SNK_Makindu_biberon_26
                  16, #Exterieur2
                  21, #SNF_biberon_26
                  16) #SNK_Makindu_cage_21
paramDuration <- 60
numSensors <- 8

# code
# -----------------------------------------------------------------------------

bdd <- lapply(files, function(myFile){
	read.table(myFile, header = TRUE, sep = ";", dec = ".")
})
bdd <- do.call(rbind, bdd)
bdd$dateTime <- as.POSIXlt(paste0(bdd$year, "-", bdd$month, "-", #Ajout d'une colonne avec la date et l'heure au format POSIX
	bdd$day, " ", bdd$hour, ":", bdd$minute, ":", bdd$second))
bdd$temperature[bdd$temperature == 85.0] <- NA #Si le captur bug la temp est à 85 du coup remplacé par NA

bdd$sensorId <- as.character(bdd$sensorId)

bdd$sensorId[bdd$sensorId == "28-00000ac82be5"] <- "SNK_Makindu_biberon_26"
bdd$sensorId[bdd$sensorId == "28-00000ac82d99"] <- "SNK_Makindu_cage_21"
bdd$sensorId[bdd$sensorId == "28-00000ac8bafe"] <- "SNF_biberon_26"
bdd$sensorId[bdd$sensorId == "28-00000ac8a098"] <- "SNF_cage_21"
bdd$sensorId[bdd$sensorId == "28-00000ac89b2d"] <- "Exterieur1"
bdd$sensorId[bdd$sensorId == "28-00000ac8aa0f"] <- "Exterieur2"
bdd$sensorId[bdd$sensorId == "28-00000ac85b0c"] <- "SNK_Kobodo_biberon_26"
bdd$sensorId[bdd$sensorId == "28-00000ac84a81"] <- "SNK_Kobodo_cage_21"

#Launch alert script if pb
trash <- sapply(seq_along(as.character(unique(bdd$sensorId))), function(i){
	mySensor <- as.character(unique(bdd$sensorId))[i]
	bddX <- bdd[bdd$sensorId == mySensor,]
	bddX <- tail(bddX, paramDuration)
	if(mean(bddX$temperature) > paramMaxTemp[i]){
		try(system(paste0(
			"python3 emailSender_XX.py ", 
			round(mean(bddX$temperature, na.rm = TRUE), 
			digits = 1), " ", bddX$sensorId[1]), intern = TRUE, ignore.stderr = TRUE))
	}else{
		if(mean(bddX$temperature) < paramMinTemp[i]){
			try(system(paste0(
				"python3 emailSender_XX.py ", 
				round(mean(bddX$temperature, na.rm = TRUE), 
				digits = 1), " ", bddX$sensorId[1]), intern = TRUE, ignore.stderr = TRUE))
		}
	}
})


