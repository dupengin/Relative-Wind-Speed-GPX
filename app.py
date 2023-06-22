from flask import Flask, render_template
import folium
import branca.colormap as cm
from folium import plugins


import matplotlib.pyplot as plot
import io
import base64

from windSpeedRequest import requestWeatherData
from relWindSpeed import relWindSpeed
from saveData import saveDataCSV
from speedDirectionCalc import speedDirectionCalculator
from movingPointAve import movingPointAve






app = Flask(__name__)





@app.route('/')
def index():
    
    headWind, ex_data = get_data()

    # Generate map
    map_heatmap = generate_line(ex_data, headWind)

    #graph = generate_graph(headWind, ex_data)

    # Render the map in HTML template
    return render_template('heatmap.html', map_heatmap=map_heatmap._repr_html_())

def get_data():
    testMode = True
    usrBearing, usrSpeed, ex_data = speedDirectionCalculator('filesGPX/2023-06-17_1171709424_Cycling.gpx')
    windSpeeds, windDirs = requestWeatherData(ex_data, testMode)

    headWind, windResDir, windResSpeed = relWindSpeed(usrSpeed, usrBearing, windSpeeds, windDirs)
    ex_data, headWind = movingPointAve(ex_data, headWind)
    saveDataCSV(ex_data, headWind, usrBearing, usrSpeed, windResSpeed, windResDir)
    

    
    
    return(headWind, ex_data)


def generate_line(ex_data, headWind):
    #centre point will be set to the coords in the middle of the data array
    lat_c = ex_data[int(len(ex_data)/2)]["lat"]
    lon_c = ex_data[int(len(ex_data)/2)]["longit"]
    

    # Create a folium map centered on the uk 
    map_line = folium.Map(location=[lat_c, lon_c], zoom_start=10)

    # Create a colormap for the line color based on variable x
    colormap = cm.LinearColormap(colors=['blue','white', 'red'], vmin=min(headWind), vmax=max(headWind))
    coord=[]
    color = []
    # Add lines to the map
    for i in range (int(len(ex_data)-1)):
        t = (ex_data[i]["lat"], ex_data[i]["longit"])
        coord.append(t)
        
    for i in range(len(coord)-1):
        seg_coord = coord[i:i+2]
        color = colormap(headWind[i])
        polyline = folium.PolyLine(locations = seg_coord,color = color, weight = 3)
        wind_textpath = plugins.PolyLineTextPath(
        polyline, " > ", repeat=True, offset=7, attributes={"fill": "#000000", "font-weight": "bold", "font-size": "24"})
        map_line.add_child(polyline)
        map_line.add_child(wind_textpath)

    
        
    



    # Add the colormap to the map
    colormap.caption = 'HeadWind'
    colormap.add_to(map_line)

    
    return map_line


def generate_graph( headWind, ex_data):

    timeSecs = []

    for i in range (len(ex_data)-1):
        t = ex_data[i]['time']
        hours, mins, secs = t.split(":")
        tSecs = (hours * 3600) + (mins * 60) + secs
        timeSecs.append(tSecs)
    
    x = headWind
    y = timeSecs

    plot.scatter(x , y)
    plot.xlabel ('X')
    plot.ylabel ('Y')
    plot.title('Head Wind Graph')

    img = io.BytesIO()
    plot.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return (plot_url)
    
    



if __name__ == '__main__':
    app.run(debug=True)
