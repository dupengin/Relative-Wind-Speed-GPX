"""The following code calls out the weather.visualcrossing.com api service to gather weather data for the required date
The returned json packet includes weather conditions for each hour of the day, i.e each date has 24 arrays of weather data
 """
def requestWeatherData(ex_data):

    import requests

    windSpeeds = []
    windDirs = []

    apiKey = 'UATQGJWXG8AYRFTJTJWEWAV4H'
    y = round(len(ex_data)/2)
    latitude = ex_data[y]['lat'] 
    longitude = ex_data[y]['longit']

    date = ex_data[y]['date']
    time = ex_data[y]['time']

    #data is recorded to the nearest hour,therefore time shall be rounded to the nearest hour
    hours, mins, secs = time.split(":")

    x = round(int(mins)/60 + int(secs)/3600)

    hoursTotal = int(hours) + x

    endpoint = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{longitude},{latitude}/{date}?key={apiKey}'

    response = requests.get(endpoint, timeout = 20)
    dataWeather = response.json()



    for i in range (len(ex_data) - 1):

        time = ex_data[i]['time']
        hours, mins, secs = time.split(":")

        x = round(int(mins)/60 + int(secs)/3600)

        hoursTotal = int(hours) + x

        
        windSpeeds.append( dataWeather['days'][0]['hours'][hoursTotal]['windspeed'])
        windDirs.append( dataWeather['days'][0]['hours'][hoursTotal]['winddir'])

    return (windSpeeds, windDirs)
    





