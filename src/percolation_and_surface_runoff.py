import geopandas as gpd
import json
import matplotlib.pyplot as plt

# Load GeoJSON data
gdf = gpd.read_file('data/Sub_basins.geojson')


def load_percolation_surface():
    # Load percolation and surface runoff ranges
    with open('data/percolation_data.json', 'r') as f:
        percolation_ranges = json.load(f)

    with open('data/surface_runoff_data.json', 'r') as f:
        surface_runoff_ranges = json.load(f)

    return gdf, percolation_ranges, surface_runoff_ranges


def plot_percolation_surface(frame, ax1, ax2, gdf, percolation_ranges, surface_runoff_ranges):
    month = list(percolation_ranges.keys())[frame]

    # Get percolation and surface runoff values
    percolation_values = [percolation_ranges[month][str(i + 1)] for i in range(len(gdf))]
    surface_runoff_values = [surface_runoff_ranges[month][str(i + 1)] for i in range(len(gdf))]

    # Plot percolation ranges
    ax1.clear()
    gdf['ET'] = percolation_values
    gdf.plot(column='ET', cmap='Blues', linewidth=0.8, ax=ax1, edgecolor='black', legend=False)
    ax1.set_title(f'Percolation')
    ax1.set_axis_off()

    # Plot surface runoff ranges
    ax2.clear()
    gdf['ET'] = surface_runoff_values
    gdf.plot(column='ET', cmap='Greens', linewidth=0.8, ax=ax2, edgecolor='black', legend=False)
    ax2.set_title(f'Surface Runoff')
    ax2.set_axis_off()

    return month
