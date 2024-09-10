import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import json

# Load GeoJSON data from three files
gdf = gpd.read_file('data/Sub_basins.geojson')

# Load ET ranges from JSON files
with open('data/percolation_data.json', 'r') as f:
    percolation_ranges = json.load(f)

with open('data/surface_runoff_data.json', 'r') as f:
    surface_runoff_ranges = json.load(f)

with open('data/et_vis_data.json', 'r') as f:
    et_ranges = json.load(f)

# Create a figure and axes for the animation
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(30, 10))


def update(frame):
    # Get month name
    month = list(percolation_ranges.keys())[frame]

    # Get ET values for percolation_ranges
    percolation_values = [percolation_ranges[month][str(i + 1)] for i in range(len(gdf))]

    # Get ET values for surface_runoff_ranges
    surface_runoff_values = [surface_runoff_ranges[month][str(i + 1)] for i in range(len(gdf))]

    # Get ET values for third_ranges
    third_values = [et_ranges[month][str(i + 1)] for i in range(len(gdf))]

    # Clear previous plots
    ax1.clear()
    ax2.clear()
    ax3.clear()

    # Plot percolation_ranges
    gdf['ET'] = percolation_values
    gdf.plot(column='ET', cmap='Blues', linewidth=0.8, ax=ax1, edgecolor='black', legend=False)
    ax1.set_title(f'Percolation for {month}')
    ax1.set_axis_off()

    # Plot surface_runoff_ranges
    gdf['ET'] = surface_runoff_values
    gdf.plot(column='ET', cmap='Greens', linewidth=0.8, ax=ax2, edgecolor='black', legend=False)
    ax2.set_title(f'Surface Runoff for {month}')
    ax2.set_axis_off()

    # Plot third_ranges
    gdf['ET'] = third_values
    gdf.plot(column='ET', cmap='Oranges', linewidth=0.8, ax=ax3, edgecolor='black', legend=False)
    ax3.set_title(f'Third Metric for {month}')
    ax3.set_axis_off()


# Create animation
ani = animation.FuncAnimation(fig, update, frames=len(percolation_ranges), repeat=False)

# Save the animation using Pillow
ani.save('et_values_animation.gif', writer='pillow')

# Show the plot
plt.show()
