
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

# Constants
rho_values = {
    "9 km": 0.467,  # kg/m³
    "6 km": 0.6601,  # kg/m³
    "3 km": 0.9093  # kg/m³
}
g = 9.81  # Gravitational acceleration (m/s²)

# Rocketman parachute sizes
sizes_in = [24, 30, 36, 48, 60, 72, 84, 96, 108, 120, 144, 168, 192, 216, 240, 288, 360]
sizes_m = np.array([size * 2.54e-2 for size in sizes_in])  # Convert inches to meters

# Calculate diameter for which weight = drag
def calculate_diameter(mass, drag_coef, v_desc, rho):
    radius = np.sqrt((2 * mass * g) / (drag_coef * rho * np.pi * v_desc**2))
    return 2 * radius  # Diameter = 2 * Radius

# Function to update the plot
def update_plot():
    try:
        # Get input values
        min_mass = float(entry_min_mass.get())
        max_mass = float(entry_max_mass.get())
        altitude = combo_altitude.get()
        v_desc = float(entry_v_desc.get())
        drag_coef = float(entry_drag_coef.get())
        
        # Get corresponding air density
        rho = rho_values[altitude]
        
        # Calculate mass range and diameters
        masses = np.linspace(min_mass, max_mass, 100)
        diameters = calculate_diameter(masses, drag_coef, v_desc, rho)
        
        # Filter valid parachute sizes
        valid_sizes = sizes_m[(sizes_m >= min(diameters)) & (sizes_m <= max(diameters))]
        valid_labels = [sizes_in[i] for i, size in enumerate(sizes_m) if size in valid_sizes]

        # Clear previous plot
        ax.clear()

        # Add dashed lines for parachute sizes and their labels
        for size, label in zip(valid_sizes, valid_labels):
            ax.axhline(size, color='black', linestyle='--', linewidth=0.5)
            ax.text(max_mass + 0.5, size, f"{label} in", 
                    verticalalignment='center', fontsize=8, color='black')

        # Plot main curve
        ax.plot(masses, diameters, color='xkcd:dark blue', linestyle='-')
        
        # Dynamically adjust axis limits
        ax.set_xlim(min_mass, max_mass)
        ax.set_ylim(min(diameters) - 0.1, max(diameters) + 0.1)

        # Set labels and title
        ax.set_xlabel('Rocket Mass [kg]')
        ax.set_ylabel('Parachute Diameter [m]')
        ax.set_title(f'Descent Velocity: {v_desc} m/s')

        # Add gridlines and ticks
        ax.grid(which='major', color='xkcd:dark blue', alpha=0.2, linewidth=0.6)
        ax.grid(which='minor', color='xkcd:dark blue', alpha=0.1, linewidth=0.2)
        ax.minorticks_on()
        ax.tick_params(which='both', direction='in', top=True, right=True)

        # Redraw the canvas
        canvas.draw()

    except ValueError:
        # Handle invalid input
        tk.messagebox.showerror("Invalid Input", "Please enter valid numeric values.")

# Tkinter setup
root = tk.Tk()
root.title("Parachute Sizing")

# Input fields
inputs = [
    ("Minimum Mass (kg)", "40.0"),
    ("Maximum Mass (kg)", "80.0"),
    ("Descent Velocity (m/s)", "9.0"),
    ("Drag Coefficient", "2.2")
]

# Create input labels and entry widgets
entries = {}
for i, (label_text, default) in enumerate(inputs):
    ttk.Label(root, text=label_text).grid(row=i, column=0, padx=5, pady=2, sticky="w")
    entry = ttk.Entry(root)
    entry.insert(0, default)
    entry.grid(row=i, column=1, padx=5, pady=2)
    entries[label_text] = entry

entry_min_mass = entries["Minimum Mass (kg)"]
entry_max_mass = entries["Maximum Mass (kg)"]
entry_v_desc = entries["Descent Velocity (m/s)"]
entry_drag_coef = entries["Drag Coefficient"]

# Dropdown for altitude
ttk.Label(root, text="Apogee Altitude").grid(row=len(inputs), column=0, padx=5, pady=2, sticky="w")
combo_altitude = ttk.Combobox(root, values=list(rho_values.keys()))
combo_altitude.set("9 km")  # Default altitude
combo_altitude.grid(row=len(inputs), column=1, padx=5, pady=2)

# Plotting area
fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=2, rowspan=len(inputs) + 1, padx=10, pady=10)

# Update button
update_button = ttk.Button(root, text="Update Plot", command=update_plot)
update_button.grid(row=len(inputs) + 1, column=1, pady=10)

root.mainloop()
