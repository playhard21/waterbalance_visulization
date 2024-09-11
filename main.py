import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Import from the src folder
from src.percolation_and_surface_runoff import load_percolation_surface, plot_percolation_surface
from src.evapotraspiration import load_et_values, plot_et

# Set the plot type (et or percolation_and_surface<<9
plot_type = 'et'

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
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    import numpy as np

    # Import from the src folder
    from src.percolation_and_surface_runoff import load_percolation_surface, plot_percolation_surface
    from src.evapotraspiration import load_et_values, plot_et

    # Set the plot type
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
        fig, (ax1, ax2, cax) = plt.subplots(1, 3, figsize=(20, 10), gridspec_kw={'width_ratios': [1, 1, 0.05]})


        def update(frame):
            # Plot percolation and surface runoff
            month = plot_percolation_surface(frame, ax1, ax2, gdf, percolation_ranges, surface_runoff_ranges)
            fig.suptitle(f'Month: {month}', fontsize=20)

    elif plot_type == 'et':
        # Load data for evapotranspiration
        gdf, percolation_ranges, surface_runoff_ranges = load_percolation_surface()  # We only need gdf
        et_ranges = load_et_values()

        # Calculate global min and max
        global_min, global_max = get_global_min_max(percolation_ranges, surface_runoff_ranges, et_ranges)

        # Create a figure with one subplot for evapotranspiration and a colorbar axis
        fig, (ax3, cax) = plt.subplots(1, 2, figsize=(12, 10), gridspec_kw={'width_ratios': [1, 0.05]})


        def update(frame):
            # Plot ET values
            month = plot_et(frame, ax3, gdf, et_ranges)
            fig.suptitle(f'Month: {month}', fontsize=20)

    # Set the color limits for consistency across frames
    norm = plt.Normalize(vmin=global_min, vmax=global_max)

    # Create a colorbar
    sm = plt.cm.ScalarMappable(cmap='Oranges' if plot_type == 'et' else 'Blues', norm=norm)
    sm.set_array([])  # Required for colorbar
    fig.colorbar(sm, cax=cax)

    # Create animation
    ani = animation.FuncAnimation(fig, update,
                                  frames=len(
                                      percolation_ranges if plot_type == 'percolation_and_surface' else et_ranges),
                                  repeat=False)

    # Save the animation using Pillow
    ani.save(f'{plot_type}_animation_with_scale.gif', writer='pillow')

    # Show the plot
    plt.show()
    # Create a figure with one subplot for evapotranspiration
    fig, ax3 = plt.subplots(1, 1, figsize=(10, 10))


    def update(frame):
        # Plot ET values
        month = plot_et(frame, ax3, gdf, et_ranges)
        fig.suptitle(f'{month}', fontsize=20)

# Create animation
ani = animation.FuncAnimation(fig, update,
                              frames=len(percolation_ranges if plot_type == 'percolation_and_surface' else et_ranges),
                              repeat=False)

# Save the animation using Pillow
ani.save(f'{plot_type}_animation.gif', writer='pillow')

# Show the plot
plt.show()
