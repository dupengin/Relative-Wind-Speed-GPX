"""
Calculation of the speed and direction from the GPX file
Methodology:
- Extract gpx data using parsing code created by others - https://pypi.org/project/gpxpy/
- Calculate the direction of the user and speed based on the gpx data
    Where i is a row in the gpx data
    The direction and distance will be calcualted using the coord at i + 1
    This direction will then be the direction at time in row i
    The time difference between i + 1 and i will be used with the distance to give a resulting speed 
- store the direction and speed in a new array

Assumptions:
- it is assumed that there is no acceleration between each long and latitude coordinate, they are traveling at a constant speed over this short distance

"""

from windSpeedRequest import requestWeatherData
from relWindSpeed import relWindSpeed
from saveData import saveDataCSV
from app import index


def speedDirectionCalculator(fileGPX):
    import gpxpy
    import gpxpy.gpx
    import math
    

    gpx_file = open(fileGPX, 'r')
    gpx_data = gpxpy.parse(gpx_file)

    #create 2D array to store extracted data
    global ex_data
    ex_data = []
    
    for track in gpx_data.tracks:
        for segment in track.segments:
            for point in segment.points:
                time = point.time.strftime("%H:%M:%S")
                date = point.time.strftime("%Y-%m-%d")
                longitude = point.longitude
                latitude = point.latitude

                ex_data.append({'time':time, 'date':date, 'longit':longitude, 'lat':latitude})


    bearings, speed = bearingDistance(ex_data) #bearings is in deg and speed in m/s

    return (bearings, speed)
    
    


def bearingDistance(ex_data):
    import math
    bearings=[]
    dist=[]
    diffTimes = []
    speed = []

    for i in range (len(ex_data)-1):
        lat1 = math.radians(ex_data[i]['lat'])
        lat2 = math.radians(ex_data[i+1]['lat'])
        long1 = math.radians(ex_data[i]['longit'])
        long2 = math.radians(ex_data[i+1]['longit'])
        time1 = ex_data[i]['time']
        time2 = ex_data[i+1]['time']

        diffLong = long2 - long1
        diffLat = lat2 - lat1
        
        x = math.sin(diffLong) * math.cos(lat2)
        
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

        initial_bearing = math.atan2(x, y)

        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360
        

        R = 6371e3 #Radius of earth in metres
        a = (math.sin(diffLat/2) * math.sin(diffLat/2)) + (math.cos(lat1) * math.cos(lat2) * (math.sin(diffLong/2) * math.sin(diffLong/2)))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c #distance in metres

        bearings.append(compass_bearing)
        dist.append(distance)

        hours1, mins1, secs1 = time1.split(":")
        hours2, mins2, secs2 = time2.split(":")

        seconds1 = (int(hours1) * 3600) + (int(mins1) * 60) + int(secs1)
        seconds2 = (int(hours2) * 3600) + (int(mins2) * 60) + int(secs2) 
        diffTime = seconds2 - seconds1
        diffTimes.append(diffTime)

        if diffTime == 0 :
            diffTime = 0.1
        

       

        speed.append(distance / diffTime)

  

    return (bearings,speed) #bearings is in deg and speed is in m/s
    




usrBearing, usrSpeed = speedDirectionCalculator('filesGPX/2023-06-17_1171709424_Cycling.gpx')
windSpeeds, windDirs = requestWeatherData(ex_data)

headWind, windResDir, windResSpeed = relWindSpeed(usrSpeed, usrBearing, windSpeeds, windDirs)
saveDataCSV(ex_data, headWind, usrBearing, usrSpeed, windResSpeed, windResDir)
index(ex_data, headWind)




"""
Following was copied from https://github.com/TechnicalVillager/distance-bearing-calculation/blob/master/distance_bearing.py


import math
R = 6371e3 #Radius of earth in metres
def distance_bearing(homeLattitude, homeLongitude, destinationLattitude, destinationLongitude):
	rlat1 = homeLattitude * (math.pi/180) 
	rlat2 = destinationLattitude * (math.pi/180) 
	rlon1 = homeLongitude * (math.pi/180) 
	rlon2 = destinationLongitude * (math.pi/180) 
	dlat = (destinationLattitude - homeLattitude) * (math.pi/180)
	dlon = (destinationLongitude - homeLongitude) * (math.pi/180)
	#haversine formula to find distance
	a = (math.sin(dlat/2) * math.sin(dlat/2)) + (math.cos(rlat1) * math.cos(rlat2) * (math.sin(dlon/2) * math.sin(dlon/2)))
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	distance = R * c #distance in metres
	#formula for bearing
	y = math.sin(rlon2 - rlon1) * math.cos(rlat2)
	x = math.cos(rlat1) * math.sin(rlat2) - math.sin(rlat1) * math.cos(rlat2) * math.cos(rlon2 - rlon1)
	bearing = math.atan2(y, x) #bearing in radians
	bearingDegrees = bearing * (180/math.pi)
	out = [distance, bearingDegrees]
	return out
"""