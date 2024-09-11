import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Import from the src folder
from src.percolation_and_surface_runoff import load_percolation_surface, plot_percolation_surface
from src.evapotraspiration import load_et_values, plot_et

# Set the plot type (et or percolation_and_surface<<9
plot_type = 'percolation_and_surface'


if plot_type == 'percolation_and_surface':
    # Load data for percolation and surface runoff
    gdf, percolation_ranges, surface_runoff_ranges = load_percolation_surface()

    # Create a figure with two subplots for percolation and surface runoff
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    def update(frame):
        # Plot percolation and surface runoff
        month = plot_percolation_surface(frame, ax1, ax2, gdf, percolation_ranges, surface_runoff_ranges)
        fig.suptitle(f'Month: {month}', fontsize=20)

elif plot_type == 'et':
    # Load data for evapotranspiration
    # Also load gdf (GeoDataFrame) here, as it's needed for plotting
    gdf, _, _ = load_percolation_surface()  # We use gdf, but ignore the other two values
    et_ranges = load_et_values()

    # Create a figure with one subplot for evapotranspiration
    fig, ax3 = plt.subplots(1, 1, figsize=(10, 10))

    def update(frame):
        # Plot ET values
        month = plot_et(frame, ax3, gdf, et_ranges)
        fig.suptitle(f'Month: {month}', fontsize=20)

# Create animation
ani = animation.FuncAnimation(fig, update,
                              frames=len(percolation_ranges if plot_type == 'percolation_and_surface' else et_ranges),
                              repeat=False)

# Save the animation using Pillow
ani.save(f'{plot_type}_animation.gif', writer='pillow')

# Show the plot
plt.show()