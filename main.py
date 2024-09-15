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
    with open('data/et_vis_data.json', 'r') as f:
        et_ranges = json.load(f)
    return gdf, et_ranges


# Define custom colormap for classified values
def get_classified_colormap(thresholds, colors):
    cmap = mcolors.ListedColormap(colors)
    norm = mcolors.BoundaryNorm(thresholds, len(colors))
    return cmap, norm


# Plot evapotranspiration values
def plot_et(frame, ax, gdf, et_ranges, norm, colormap):
    month = list(et_ranges.keys())[frame]
    et_values = [et_ranges[month][str(i + 1)] for i in range(len(gdf))]
    gdf['ET'] = et_values
    ax.clear()
    gdf.plot(column='ET', cmap=colormap, linewidth=0.8, ax=ax, edgecolor='black', legend=False, norm=norm)
    ax.set_title(f'Evapotranspiration (ET)', fontsize=16)
    ax.set_axis_off()
    return month


# Main script
gdf, et_ranges = load_data()

# Create figure and color map with custom thresholds and red palette
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
thresholds = [0, 50, 60, 70, 80, 150]
colors = ['#ffcccc', '#ff9999', '#ff6666', '#ff3333', '#ff0000']
colormap, norm = get_classified_colormap(thresholds, colors)

# Create colorbar
cbar_ax = fig.add_axes([0.88, 0.25, 0.01, 0.4])
sm = plt.cm.ScalarMappable(cmap=colormap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, cax=cbar_ax)

# Format colorbar ticks
cbar.set_ticks(thresholds)
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
ani.save('et_animation.gif', writer='pillow')
plt.show()
