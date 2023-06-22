"""The following code calls out the weather.visualcrossing.com api service to gather weather data for the required date
The returned json packet includes weather conditions for each hour of the day, i.e each date has 24 arrays of weather data
 """
def requestWeatherData(ex_data, testMode):

    import requests
    from saveData import saveTestDataCSV
    import csv

    windSpeeds = []
    windDirs = []

    #Test mode uses a pre-saved csv for wind speed and direction, this is to avoid using api requests as these are capped per day
    if (testMode):
        fileName = 'test_data_0.csv'
        print('test mode') #terminal comment to confirm that test mode is set

        with open (fileName) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                windSpeeds.append(float(row[0]))
                windDirs.append(float(row[1]))

    else:

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

        try:
            response = requests.get(endpoint, timeout=20)
            response.raise_for_status()  # Raise an exception if the request was not successful (status code >= 400)
            dataWeather = response.json()
        except requests.exceptions.HTTPError as err:
            if response.status_code == 429:
                print("Too Many Requests. Please try again later.")
            else:
                print(f"HTTP Error: {response.status_code} - {err}")
        except requests.exceptions.RequestException as err:
            print(f"An error occurred during the request: {err}")

        



        for i in range (len(ex_data) - 1):

            time = ex_data[i]['time']
            hours, mins, secs = time.split(":")

            x = round(int(mins)/60 + int(secs)/3600)

            hoursTotal = int(hours) + x

            
            windSpeeds.append( dataWeather['days'][0]['hours'][hoursTotal]['windspeed'])
            windDirs.append( dataWeather['days'][0]['hours'][hoursTotal]['winddir'])

    #saveTestDataCSV(windSpeeds, windDirs)

    return (windSpeeds, windDirs)
    





