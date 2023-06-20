

def write_lists_to_csv(filename, headers, *lists):
    import csv
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for row in zip(*lists):
            writer.writerow(row)


def saveDataCSV(ex_data, headWind, usrDir, usrSpeed, resWindSpeed, ResWindDir ):
    longitude = []
    latitude = []
    for i in range(len(ex_data)-1):
        longitude.append(ex_data[i]['longit'])
        latitude.append(ex_data[i]['lat'])
    
    filename = 'output.csv'
    headers = ['longitude', 'latitude', 'Head Wind', 'User Direction', 'User Speed', 'Resultant Wind Speed', 'Resultant Wind Direction']

    write_lists_to_csv(filename, headers, longitude, latitude, headWind, usrDir, usrSpeed, resWindSpeed, ResWindDir)



# Example lists


# Example usage


