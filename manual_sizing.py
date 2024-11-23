# Import modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

# Constants
rho_9km = 0.467  # kg/m³
rho_6km = 0.6601 # kg/m³
rho_3km = 0.9093  # kg/m³

g = 9.81
drag_coef = 2.2

v_desc = 10  # m/s

# Rocketman parachute sizes
sizes_in = [24, 30, 36, 48, 60, 72, 84, 96, 108, 120, 144, 168, 192, 216, 240, 288, 360]
sizes_m = [size * 2.54e-2 for size in sizes_in]  # Convert inches to meters
sizes_m = np.array(sizes_m)

# Calculate diameter for which weight = drag
def calculate_diameter(mass, drag_coef, v_desc, rho=rho_9km):
    radius = np.sqrt((2 * mass * g) / (drag_coef * rho * np.pi * (v_desc) ** 2))
    return 2 * radius  # Diameter = 2 * Radius

masses = np.linspace(2.5, 10)  # Rocket mass range
diameter = calculate_diameter(masses, drag_coef, v_desc, rho_6km)

# Plotting
fig, ax = plt.subplots(1, 1, figsize=(6, 4), dpi=150)

# Filter sizes within the range of min(diameter) and max(diameter)
valid_sizes = sizes_m[(sizes_m >= min(diameter)) & (sizes_m <= max(diameter))]
valid_labels = [sizes_in[i] for i, size in enumerate(sizes_m) if size in valid_sizes]

# Add dashed lines for parachute sizes and their labels
for size, label in zip(valid_sizes, valid_labels):
    ax.axhline(size, color='black', linestyle='--', linewidth=0.5)
    ax.text(masses[-1] + 4, size, f"{label} in", 
            verticalalignment='center', fontsize=8, color='black')  # Label position

# Add the main curve
ax.plot(masses, diameter, color='xkcd:dark blue', linestyle='-')

# Set axis limits and labels
ax.set_ylim(min(diameter)-0.1, max(diameter)+0.1)
ax.set_xlabel('Rocket Mass [kg]')
ax.set_ylabel('Parachute Diameter [m]')
ax.set_title(f'Descent Velocity: {v_desc} m/s')

# Add gridlines
ax.grid(which='major', color='xkcd:dark blue', alpha=0.2, linewidth=0.6)
ax.grid(which='minor', color='xkcd:dark blue', alpha=0.1, linewidth=0.2)

# Add minor ticks   
ax.minorticks_on()
ax.tick_params(which='both', direction='in', top=True, right=True)
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())

# Show the plot
plt.tight_layout()
plt.show()
