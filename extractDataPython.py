import gpxpy
import gpxpy.gpx
import math


fileGPX = 'filesGPX/2023-03-21_test_data.gpx'


gpx_file = open(fileGPX, 'r')
gpx_data = gpxpy.parse(gpx_file)

#create 2D array to store extracted data
ex_data = []




#Establish the route by extracting the longitude and latitude of the route
#elevation is not used as the wind data set is elevation independent
#for gpx in gpx_data:
for track in gpx_data.tracks:
    for segment in track.segments:
        for point in segment.points:
            time = point.time.strftime("%Y-%m-%d %H:%M:%S")
            longitude = point.longitude
            latitude = point.latitude

            ex_data.append([time, longitude, latitude])

print(ex_data)



#calcualte the orientstion of the bike by using the two coordinates
#calculate the difference between the two coordinates 
#tan(long/lat)
