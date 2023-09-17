import geopandas as gpd
import pandas as pd
import folium 
import json
from folium.plugins import Geocoder

dist = gpd.read_file("India_districts_640.shp")
dist['geometry'] = dist['geometry'].simplify(0.01)

dd= pd.read_csv("data_by_district.csv")
dd.columns=['censuscode','data','name']
geodf=pd.merge(dist,dd,on='censuscode')

dist.set_crs('EPSG:4326', inplace=True)
geodf.set_crs('EPSG:4326', inplace=True)
geojson_data = json.loads(geodf.to_json())
#print(geojson_data['features'][0])
#exit()

# Define your custom colors and bins
colors = ["#006837", "#1a9850", "#66bd63", "#fdff00", "#ffe833", "#ffc566", "#ff9933", "#f46d43", "#d73027", "#a50026", "#660000"]
bins = [0, 20, 40, 60, 90, 120, 150, 200, 250, 300, 400, 10000]

# Create a legend HTML based on the provided colors and bins
title_html = """
<div style="position: absolute; top: 10px; left: 50%; transform: translateX(-50%); background-color: white; padding: 10px; border: 2px solid gray; z-index: 1000;">
   <p style="font-weight: bold; margin: 0; text-align: center;">Day(24-h) average for Sept 14, 2023</p>
</div>
"""

legend_html = """
<div style="position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); background-color: white; border: 2px solid gray; z-index: 1000; padding: 5px;">
    <p><strong>PM2.5 (μg/m3)</strong></p>
    <div style="display: flex; flex-direction: row; align-items: center;">
        
"""

# Iterate through the bins and colors to create legend entries
for i in range(len(bins) - 2):
    color = colors[i]
    range_min = bins[i]
    range_max = bins[i + 1]
    
    # Create a legend entry for each bin/color range
    legend_entry = f'<div style="display: flex; align-items: center; margin-right: 10px;">' \
                   f'<span style="background-color: {color}; width: 20px; height: 20px; margin-right: 5px;"></span>' \
                   f'<p style="margin: 0;width: 70px">{range_min} - {range_max}</p>' \
                   f'</div>'

    # Add the legend entry to the legend HTML
    legend_html += legend_entry

# Add a legend entry for values above the last bin
color = colors[-1]
legend_entry = f'<div style="display: flex; align-items: center; margin-right: 10px;">' \
                   f'<span style="background-color: {color}; width: 20px; height: 20px; margin-right: 5px;"></span>' \
                   f'<p style="margin: 0;width: 70px">400+</p>' \
                   f'</div>'
legend_html += legend_entry

# Close the legend HTML
legend_html += "</div></div>"

# Create a color mapping function
def color_map(value):
    for i in range(len(bins) - 1):
        if bins[i] <= value <= bins[i + 1]:
            return colors[i]
    return colors[-1]  # Handle values outside the specified bins

# Set the fill color based on the 'value' property
polygon_colors = []
for idx, row in geodf.iterrows():
    value = row['data']
    color = color_map(value)
    polygon_colors.append(color)
geodf['color'] = polygon_colors

# Create Basemap
center=[28.7041,77.1025]
m = folium.Map(location=center,zoom_start=6,tiles="OpenStreetMap")

# Iterate over the polygons in the GeoDataFrame
for index, row in geodf.iterrows():
    # Get the assigned color for the current polygon
    polygon_color = row['color']
    legend_label = row['censuscode']

    # Create a Folium GeoJson object for the current polygon
    folium.GeoJson(
        row['geometry'],
        style_function=lambda x, color=polygon_color: {'fillColor': color, 'color': color, 'fillOpacity': 0.8, 'weight': 1},
    ).add_to(m)


# Add the custom legend to the map
#m.get_root().html.add_child(folium.Element(legend_html))
#m.get_root().html.add_child(folium.Element(title_html))

# Write a style_function and highlight_function that makes the layer transparent. 
style_function = lambda x: {'fillColor': '#ffffff',
                            'color':'#000000',
                            'fillOpacity': 0.1,
                            'weight':0.1}
highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}

#Create the transparent GEOJSON layer
NIL2 = folium.features.GeoJson(
    data = geodf, #Give in data that has both geometry and required variable
    style_function=style_function, 
    control=False,
    highlight_function=highlight_function, 
    tooltip=folium.features.GeoJsonTooltip(
        fields=['ST_NM', 'DISTRICT','data'],
        aliases=['State', 'District: ','PM2.5 (μg/m3): '],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    )
)

#Add the transparent layer to map
m.add_child(NIL2)
m.keep_in_front(NIL2)

Geocoder(add_marker=False, collapsed=True).add_to(m)

# Save the map as an HTML file or display it in a Jupyter Notebook
m.save('choropleth_allIndia.html')


exit()
choropleth = folium.Choropleth(
    geo_data=dist,
    name= 'Choropleth map',
    data = geojson_data,
    columns=None,
    key_on='feature.properties.censuscode',
    fill_opacity=0.7,
    line_opacity=1,
    legend_name='Pollution',
).add_to(m)

#Through Folium, we can add interactivity in an indirect method.

# Write a style_function and highlight_function that makes the layer transparent. 
style_function = lambda x: {'fillColor': '#ffffff',
                            'color':'#000000',
                            'fillOpacity': 0.1,
                            'weight':0.1}
highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}

#Create the transparent GEOJSON layer
NIL2 = folium.features.GeoJson(
    data = geodf, #Give in data that has both geometry and required variable
    style_function=style_function, 
    control=False,
    highlight_function=highlight_function, 
    tooltip=folium.features.GeoJsonTooltip(
        fields=['censuscode','data'],
        aliases=['Census Code: ','Pollution: '],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    )
)

#Add the transparent layer to map
m.add_child(NIL2)
m.keep_in_front(NIL2)

m.save('choropleth_allIndia.html')