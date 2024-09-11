import matplotlib.pyplot as plt
import matplotlib.animation as animation
from src.percolation_and_surface_runoff import load_percolation_surface, plot_percolation_surface
from src.evapotraspiration import load_et_values, plot_et

# Load data for percolation/surface runoff and ET values
gdf, percolation_ranges, surface_runoff_ranges = load_percolation_surface()
et_ranges = load_et_values()

# Create a figure and axes for the animation (separate for each type)
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(30, 10))


def update(frame):
    # Plot percolation and surface runoff
    month_perc_surface = plot_percolation_surface(frame, ax1, ax2, gdf, percolation_ranges, surface_runoff_ranges)

    # Plot ET
    month_et = plot_et(frame, ax3, gdf, et_ranges)

    # Update the main title with the current month
    fig.suptitle(f'Month: {month_perc_surface}', fontsize=20)


# Create animation
ani = animation.FuncAnimation(fig, update, frames=len(percolation_ranges), repeat=False)

# Save the animation using Pillow
ani.save('et_values_animation.gif', writer='pillow')

# Show the plot
plt.show()
