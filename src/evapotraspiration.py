import geopandas as gpd
import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Load GeoJSON data
gdf = gpd.read_file('data/Sub_basins.geojson')


def load_et_values():
    # Load ET ranges
    with open('data/percolation_data.json', 'r') as f:
        et_ranges = json.load(f)

    return et_ranges, gdf


def get_colormap():
    # Define a custom brown colormap
    color_of_graph = mcolors.LinearSegmentedColormap.from_list(
        'blue', [(0.8, 0.52, 0.25), (0.5, 0.25, 0.1)]  # Brown shades
    )
    return color_of_graph


def plot_et(frame, ax3, gdf, et_ranges):
    month = list(et_ranges.keys())[frame]

    # Get ET values
    et_values = [et_ranges[month][str(i + 1)] for i in range(len(gdf))]

    # Plot ET values
    ax3.clear()
    gdf['ET'] = et_values
    # brown_cmap = create_brown_colormap()
    color_of_graph = get_colormap()
    gdf.plot(column='ET', cmap=color_of_graph, linewidth=0.8, ax=ax3, edgecolor='black', legend=False)
    ax3.set_title(f'Precolation')
    ax3.set_axis_off()

    return month
