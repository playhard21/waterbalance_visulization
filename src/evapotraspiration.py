import geopandas as gpd
import json
import matplotlib.pyplot as plt

# Load GeoJSON data
gdf = gpd.read_file('data/Sub_basins.geojson')


def load_et_values():
    # Load ET ranges
    with open('data/et_vis_data.json', 'r') as f:
        et_ranges = json.load(f)

    return et_ranges


def plot_et(frame, ax3, gdf, et_ranges):
    month = list(et_ranges.keys())[frame]

    # Get ET values
    et_values = [et_ranges[month][str(i + 1)] for i in range(len(gdf))]

    # Plot ET values
    ax3.clear()
    gdf['ET'] = et_values
    gdf.plot(column='ET', cmap='Oranges', linewidth=0.8, ax=ax3, edgecolor='black', legend=False)
    ax3.set_title(f'Evapotranspiration')
    ax3.set_axis_off()

    return month
