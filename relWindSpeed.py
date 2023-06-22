"""
code to calculate the relative wind speed based on the direciton and speed of the user and the wind
"""


def relWindSpeed(usrSpeed, usrBearing, windSpeeds, windDirs):
    import math
    windResSpeed = []
    windResDir = []
    windResDir_deg = []
    headWind = []

    for i in range(len(usrSpeed)):
        # calculate the wind users velocity components in the x & y direciton
        usrVel_X = usrSpeed[i] * math.cos(usrBearing[i])
        usrVel_Y = usrSpeed[i] * math.sin(usrBearing[i])
        windVel_X = windSpeeds[i] * math.cos(windDirs[i]) 
        windVel_Y = windSpeeds[i] * math.cos(windDirs[i])

        # calcule the resultant wind speed

        windRes_X = windVel_X - usrVel_X
        windRes_Y = windVel_Y - usrVel_Y

        windResSpeed.append(math.sqrt((windRes_X)**2 + (windRes_Y)**2))
        windResDir.append(math.atan2(windRes_Y, windRes_X))
        windResDir_deg.append(math.degrees(windResDir[i]))

        # calculate the headwind faced by the user

        usrBearing_Rads = math.radians(usrBearing[i])
        windDir_Rads = math.radians(windDirs[i])
    
        angleRad = windDir_Rads - usrBearing_Rads
    
        headWind.append(windResSpeed[i] * math.cos(angleRad) )
    
    return (headWind, windResDir, windResSpeed) 
    
