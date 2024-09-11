import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import FuncFormatter
from src.evapotraspiration import load_et_values, plot_et, get_colormap, get_global_min_max
import geopandas as gpd
import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


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


# Calculate global min and max for the color scale
def get_global_min_max(et_ranges_values):
    all_et = np.concatenate([list(month.values()) for month in et_ranges_values.values()])

    # Calculate the global min and max values
    global_min = all_et.min()
    global_max = all_et.max()

    return global_min, global_max

# Load data for evapotranspiration
et_ranges, gdf = load_et_values()

# Calculate global min and max
global_min, global_max = get_global_min_max(et_ranges)

# Create a figure with one subplot for evapotranspiration
fig, ax3 = plt.subplots(1, 1, figsize=(12, 8))  # Reduced figure height


def update(frame):
    # Plot ET values
    month = plot_et(frame, ax3, gdf, et_ranges)
    fig.suptitle(f'{month}', fontsize=20)


# Set the color limits for consistency across frames
norm = plt.Normalize(vmin=global_min, vmax=global_max)

# Create the colorbar with a custom size
# The arguments are [left, bottom, width, height]
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
plt.subplots_adjust(wspace=0.01)  # Very small padding between the plot and the colorbar

# Create animation
ani = animation.FuncAnimation(fig, update,
                              frames=len(et_ranges),
                              interval=1000,  # 1000ms = 1 second per frame
                              repeat=False)

# Save the animation using Pillow
ani.save(f'percolation.gif', writer='pillow')

# Show the plot
plt.show()
