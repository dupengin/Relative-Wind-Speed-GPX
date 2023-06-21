from flask import Flask, render_template
import folium
import branca.colormap as cm

from windSpeedRequest import requestWeatherData
from relWindSpeed import relWindSpeed
from saveData import saveDataCSV
from speedDirectionCalc import speedDirectionCalculator
import math 



app = Flask(__name__)





@app.route('/')
def index():
    
    headWind, ex_data = get_data()

    # Generate map
    map_heatmap = generate_line(ex_data, headWind)

    # Render the map in HTML template
    return render_template('heatmap.html', map_heatmap=map_heatmap._repr_html_())

def get_data():
    testMode = True
    usrBearing, usrSpeed, ex_data = speedDirectionCalculator('filesGPX/2023-06-17_1171709424_Cycling.gpx')
    windSpeeds, windDirs = requestWeatherData(ex_data, testMode)

    headWind, windResDir, windResSpeed = relWindSpeed(usrSpeed, usrBearing, windSpeeds, windDirs)
    saveDataCSV(ex_data, headWind, usrBearing, usrSpeed, windResSpeed, windResDir)

    return(headWind, ex_data)


def generate_line(ex_data, headWind):
    #centre point will be set to the coords in the middle of the data array
    lat_c = ex_data[int(len(ex_data)/2)]["lat"]
    lon_c = ex_data[int(len(ex_data)/2)]["longit"]
    

    # Create a folium map centered on the uk 
    map_line = folium.Map(location=[lat_c, lon_c], zoom_start=10)

    # Create a colormap for the line color based on variable x
    colormap = cm.LinearColormap(colors=['blue', 'red'], vmin=min(headWind), vmax=max(headWind))
    coord=[]
    # Add lines to the map
    for i in range (int(len(ex_data)-1)):
        t = (ex_data[i]["lat"], ex_data[i]["longit"])
        coord.append(t)
        
        color = colormap(headWind[i])
        folium.PolyLine(locations = [coord],color = color).add_to(map_line)


    # Add the colormap to the map
    colormap.caption = 'HeadWind'
    colormap.add_to(map_line)

    return map_line

if __name__ == '__main__':
    app.run(debug=True)
