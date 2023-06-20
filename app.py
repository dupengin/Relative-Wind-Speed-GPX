from flask import Flask, render_template
import folium
import folium.plugins as plugins #wierd bug requires this import to fix issue with folium.plugins not being found
import branca.colormap as cm

app = Flask(__name__)



@app.route('/')
def index(ex_data, headWind):
    # Generate map
    map_heatmap = generate_line(ex_data, headWind)

    # Render the map in HTML template
    return render_template('heatmap.html', map_heatmap=map_heatmap._repr_html_())

def generate_line(ex_data, headWind):
    #centre point will be set to the coords in the middle of the data array
    lat_c = ex_data[round(len(ex_data)/2)]["lat"]
    lon_c = ex_data[round(len(ex_data)/2)]["longit"]
    

    # Create a folium map centered on the uk 
    map_line = folium.Map(location=[lat_c, lon_c], zoom_start=11)

    # Create a colormap for the line color based on variable x
    colormap = cm.LinearColormap(colors=['blue', 'red'], vmin=0, vmax=1)

    # Add lines to the map
    for i in range (len(ex_data)-1):
        lat = ex_data[i]["lat"]  
        lon = ex_data[i]["longit"]
        color = colormap(headWind[i])
        folium.PolyLine(
            locations=[(lat, lon)],
            color=color,
            weight=10,
            opacity=1,
        ).add_to(map_line)

    # Add the colormap to the map
    colormap.caption = 'HeadWind'
    colormap.add_to(map_line)

    return map_line

if __name__ == '__main__':
    app.run(debug=True)
