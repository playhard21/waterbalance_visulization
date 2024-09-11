import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import FuncFormatter
import geopandas as gpd
import json
import matplotlib.colors as mcolors
import numpy as np


# Load GeoDataFrame and ET values
def load_data():
    gdf = gpd.read_file('data/Sub_basins.geojson')
    with open('data/surface_runoff_data.json', 'r') as f:
        et_ranges = json.load(f)
    return gdf, et_ranges


# take colors from here
"""
'brown', [(0.8, 0.52, 0.25), (0.5, 0.25, 0.1)]  # Brown shades
'skyblue', [(0.6, 0.8, 1.0), (0.2, 0.6, 1.0)]  # Sky blue shades
'red', [(1.0, 0.8, 0.8), (1.0, 0.2, 0.2)]  # Red shades


Runoff
Percolation
Evapotranspiration
"""


# Define custom colormap
def get_colormap(name, colors):
    return mcolors.LinearSegmentedColormap.from_list(name, colors)


# Plot evapotranspiration values
def plot_et(frame, ax, gdf, et_ranges, norm, colormap):
    month = list(et_ranges.keys())[frame]
    et_values = [et_ranges[month][str(i + 1)] for i in range(len(gdf))]
    gdf['ET'] = et_values
    ax.clear()
    gdf.plot(column='ET', cmap=colormap, linewidth=0.8, ax=ax, edgecolor='black', legend=False, norm=norm)
    # step - 02 change the name here
    ax.set_title(f'Runoff')
    ax.set_axis_off()
    return month


# Calculate global min and max for the color scale
def get_global_min_max(et_ranges):
    all_et = np.concatenate([list(month.values()) for month in et_ranges.values()])
    return all_et.min(), all_et.max()


# Main script
gdf, et_ranges = load_data()
global_min, global_max = get_global_min_max(et_ranges)

# Create figure and color map
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
# step - 03 change the name here
colormap = get_colormap('skyblue', [(0.6, 0.8, 1.0), (0.2, 0.6, 1.0)])
norm = plt.Normalize(vmin=global_min, vmax=global_max)

# Create colorbar
cbar_ax = fig.add_axes([0.88, 0.25, 0.01, 0.4])
sm = plt.cm.ScalarMappable(cmap=colormap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, cax=cbar_ax)

# Format colorbar ticks
cbar.ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x)}mm'))

# Adjust figure layout
plt.subplots_adjust(wspace=-2)


# Update function for animation
def update(frame):
    month = plot_et(frame, ax, gdf, et_ranges, norm, colormap)
    fig.suptitle(f'{month}', fontsize=20)


# Create animation
ani = animation.FuncAnimation(fig, update, frames=len(et_ranges), interval=1000, repeat=False)

# Save and show animation
# step - 04 change the name here
ani.save('percolation.gif', writer='pillow')
plt.show()
