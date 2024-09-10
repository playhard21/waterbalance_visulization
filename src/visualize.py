# src/visualize.py
import geopandas as gpd
import matplotlib.pyplot as plt
import folium

def plot_with_matplotlib(geojson_file):
    # Load the GeoJSON file
    gdf = gpd.read_file(geojson_file)
    # Plot the data with matplotlib
    gdf.plot()
    plt.show()

def plot_with_folium(geojson_file, output_html='map.html'):
    # Load the GeoJSON file
    gdf = gpd.read_file(geojson_file)
    # Create a Folium map centered on the data
    m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=10)
    # Add GeoJSON data to the map
    folium.GeoJson(gdf).add_to(m)
    # Save as HTML
    m.save(output_html)
    return