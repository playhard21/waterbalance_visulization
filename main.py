import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import FuncFormatter
import geopandas as gpd
import json
import matplotlib.colors as mcolors
import numpy as np

gdf = gpd.read_file('data/Sub_basins.geojson')


def load_et_values():
    # Load ET ranges
    # step - 01
    with open('data/et_vis_data.json', 'r') as f:
        et_ranges = json.load(f)
    return et_ranges, gdf


# take colors from here
"""
'brown', [(0.8, 0.52, 0.25), (0.5, 0.25, 0.1)]  # Brown shades
'skyblue', [(0.6, 0.8, 1.0), (0.2, 0.6, 1.0)]  # Sky blue shades
'red', [(1.0, 0.8, 0.8), (1.0, 0.2, 0.2)]  # Red shades


Runoff
Percolation
Evapotranspiration
"""


def get_colormap():
    # Define a custom brown colormap
    color_of_graph = mcolors.LinearSegmentedColormap.from_list(
        # step - 02 paste the color here
        'red', [(1.0, 0.8, 0.8), (1.0, 0.2, 0.2)]  # Red shades
    )
    return color_of_graph


def plot_et(frame, ax3, gdf, et_ranges, norm):
    month = list(et_ranges.keys())[frame]

    # Get ET values
    et_values = [et_ranges[month][str(i + 1)] for i in range(len(gdf))]

    # Plot ET values
    ax3.clear()
    gdf['ET'] = et_values
    color_of_graph = get_colormap()
    gdf.plot(column='ET', cmap=color_of_graph, linewidth=0.8, ax=ax3, edgecolor='black', legend=False, norm=norm)
    # step - 03 change the name here
    ax3.set_title(f'Evapotranspiration')
    ax3.set_axis_off()

    return month


# Calculate global min and max for the color scale
def get_global_min_max(et_ranges_values):
    all_et = np.concatenate([list(month.values()) for month in et_ranges_values.values()])
    global_min = all_et.min()
    global_max = all_et.max()
    return global_min, global_max


# Load data for evapotranspiration
et_ranges, gdf = load_et_values()

# Calculate global min and max
global_min, global_max = get_global_min_max(et_ranges)

# Create a figure with one subplot for evapotranspiration
fig, ax3 = plt.subplots(1, 1, figsize=(12, 8))  # Reduced figure height

# Set the color limits for consistency across frames
norm = plt.Normalize(vmin=global_min, vmax=global_max)


def update(frame):
    # Plot ET values
    month = plot_et(frame, ax3, gdf, et_ranges, norm)
    fig.suptitle(f'{month}', fontsize=20)


# Create the colorbar with a custom size
cbar_ax = fig.add_axes([0.88, 0.25, 0.01, 0.4])  # Adjust height and place the colorbar as close as possible

# Create the colorbar
color_of_graph = get_colormap()
sm = plt.cm.ScalarMappable(cmap=color_of_graph, norm=norm)
sm.set_array([])  # Required for colorbar
cbar = fig.colorbar(sm, cax=cbar_ax)


# Add the unit "MM" to each tick label
def add_mm_to_ticks(x, _):
    return f'{int(x)}mm'  # Converts tick values to strings with 'MM' appended


# Set tick labels with "MM" after each value
cbar.ax.yaxis.set_major_formatter(FuncFormatter(add_mm_to_ticks))

# Minimize padding between the plot and colorbar
plt.subplots_adjust(wspace=-2)  # Very small padding between the plot and the colorbar

# Create animation
ani = animation.FuncAnimation(fig, update,
                              frames=len(et_ranges),
                              interval=1000,  # 1000ms = 1 second per frame
                              repeat=False)

# Save the animation using Pillow
# Step - 04 change the name of the gif here
ani.save(f'Evapotranspiration.gif', writer='pillow')

# Show the plot
plt.show()
