import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.ticker import FuncFormatter
from src.percolation_and_surface_runoff import load_percolation_surface, plot_percolation_surface
from src.evapotraspiration import load_et_values, plot_et

# Set the plot type (et or percolation_and_surface)
plot_type = 'et'

# Calculate global min and max for the color scale
def get_global_min_max(percolation_ranges, surface_runoff_ranges, et_ranges):
    # Combine all values across all months for each dataset
    all_percolation = np.concatenate([list(month.values()) for month in percolation_ranges.values()])
    all_surface_runoff = np.concatenate([list(month.values()) for month in surface_runoff_ranges.values()])
    all_et = np.concatenate([list(month.values()) for month in et_ranges.values()])

    # Calculate the global min and max values
    global_min = min(all_percolation.min(), all_surface_runoff.min(), all_et.min())
    global_max = max(all_percolation.max(), all_surface_runoff.max(), all_et.max())

    return global_min, global_max

if plot_type == 'percolation_and_surface':
    # Load data for percolation and surface runoff
    gdf, percolation_ranges, surface_runoff_ranges = load_percolation_surface()

    # Load ET values to get global min and max values
    et_ranges = load_et_values()

    # Calculate global min and max
    global_min, global_max = get_global_min_max(percolation_ranges, surface_runoff_ranges, et_ranges)

    # Create a figure with two subplots for percolation and surface runoff
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    def update(frame):
        # Plot percolation and surface runoff
        month = plot_percolation_surface(frame, ax1, ax2, gdf, percolation_ranges, surface_runoff_ranges)
        fig.suptitle(f'{month}', fontsize=20)

elif plot_type == 'et':
    # Load data for evapotranspiration
    gdf, percolation_ranges, surface_runoff_ranges = load_percolation_surface()  # Only gdf is needed
    et_ranges = load_et_values()

    # Calculate global min and max
    global_min, global_max = get_global_min_max(percolation_ranges, surface_runoff_ranges, et_ranges)

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
    sm = plt.cm.ScalarMappable(cmap='Oranges' if plot_type == 'et' else 'Blues', norm=norm)
    sm.set_array([])  # Required for colorbar
    cbar = fig.colorbar(sm, cax=cbar_ax)

    # Add the unit "MM" to each tick label
    def add_mm_to_ticks(x, _):
        return f'{int(x)} MM'  # Converts tick values to strings with 'MM' appended

    # Set tick labels with "MM" after each value
    cbar.ax.yaxis.set_major_formatter(FuncFormatter(add_mm_to_ticks))

# Minimize padding between the plot and colorbar
plt.subplots_adjust(wspace=0.01)  # Very small padding between the plot and the colorbar

# Create animation
ani = animation.FuncAnimation(fig, update,
                              frames=len(percolation_ranges if plot_type == 'percolation_and_surface' else et_ranges),
                              interval=1000,  # 1000ms = 1 second per frame
                              repeat=False)

# Save the animation using Pillow
ani.save(f'{plot_type}_animation_with_scale.gif', writer='pillow')

# Show the plot
plt.show()