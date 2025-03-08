import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

# Constants
g = 9.81  # Gravitational acceleration (m/s²)

# Rocketman parachute sizes
sizes_in = [24, 30, 36, 48, 60, 72, 84, 96, 108, 120, 144, 168, 192, 216, 240, 288, 360]
sizes_m = np.array([size * 2.54e-2 for size in sizes_in])  # Convert inches to meters


# --- Calculation Functions ---

def air_density(altitude):
    rho0 = 1.225  # Sea-level air density in kg/m^3
    T0 = 288.15  # Sea-level standard temperature in K
    Lapse_rate = 0.0065  # Temperature lapse rate in K/m
    R = 287.05  # Specific gas constant for dry air in J/(kg·K)
    g = 9.81  # m/s^2 (gravitational acceleration)
    
    T = T0 - Lapse_rate * altitude
    P = rho0 * R * T0 * (1 - Lapse_rate * altitude / T0) ** (g / (R * Lapse_rate))
    rho = P / (R * T)
    return max(rho, 0)

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
        altitude = float(entry_altitude.get())
        v_desc = float(entry_v_desc.get())
        drag_coef = float(entry_drag_coef.get())
        
        # Get corresponding air density
        rho = air_density(altitude)
        
        # Update air density label
        air_density_label.config(text=f"Air Density: {rho:.4f} kg/m³")
        
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
            ax.axhline(size, color='black', linestyle='--', linewidth=0.3)
            ax.text(max_mass + 0.5, size, f"{label} in", 
                    verticalalignment='center', fontsize=4, color='black')

        # Plot main curve
        ax.plot(masses, diameters, color='xkcd:dark blue', linestyle='-')
        
        # Dynamically adjust axis limits
        ax.set_xlim(min_mass, max_mass)
        ax.set_ylim(min(diameters) - 0.1, max(diameters) + 0.1)

        # Set labels and title
        ax.set_xlabel('Rocket Mass [kg]', fontsize=4)
        ax.set_ylabel('Parachute Diameter [m]', fontsize=4)
        ax.set_title(f'Descent Velocity: {v_desc} m/s', fontsize=6)

        # Add gridlines and ticks
        ax.grid(which='major', color='xkcd:dark blue', alpha=0.2, linewidth=0.2)
        ax.grid(which='minor', color='xkcd:dark blue', alpha=0.1, linewidth=0.1)
        ax.minorticks_on()
        ax.tick_params(labelsize=4, which='both', direction='in', top=True, right=True, width=0.3)

        # Redraw the canvas
        canvas.draw_idle()

    except ValueError:
        # Handle invalid input
        tk.messagebox.showerror("Invalid Input", "Please enter valid numeric values.")

# Tkinter setup
root = tk.Tk()
root.title("Parachute Sizing")

# Create a frame for the canvas and scrollbar
frame = ttk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew")

# Create a canvas and add a scrollbar
canvas_frame = tk.Canvas(frame)
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas_frame.yview)
canvas_frame.configure(yscrollcommand=scrollbar.set)

# Pack the canvas and scrollbar
canvas_frame.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Create another frame inside the canvas
inner_frame = ttk.Frame(canvas_frame)
canvas_frame.create_window((0, 0), window=inner_frame, anchor="nw")

# Update the scroll region when the inner frame changes size
def on_frame_configure(event):
    canvas_frame.configure(scrollregion=canvas_frame.bbox("all"))

inner_frame.bind("<Configure>", on_frame_configure)

# Create input labels and entry widgets
inputs = [
    ("Minimum Mass (kg)", "40.0"),
    ("Maximum Mass (kg)", "100.0"),
    ("Descent Velocity (m/s)", "7.5"),
    ("Drag Coefficient", "2.2"),
    ("Altitude (km)", "0")
]

entries = {}
for i, (label_text, default) in enumerate(inputs):
    ttk.Label(inner_frame, text=label_text).grid(row=i, column=0, padx=5, pady=2, sticky="w")
    entry = ttk.Entry(inner_frame)
    entry.insert(0, default)
    entry.grid(row=i, column=1, padx=5, pady=2, sticky="ew")
    entries[label_text] = entry

entry_min_mass = entries["Minimum Mass (kg)"]
entry_max_mass = entries["Maximum Mass (kg)"]
entry_v_desc = entries["Descent Velocity (m/s)"]
entry_drag_coef = entries["Drag Coefficient"]
entry_altitude = entries["Altitude (km)"]

# Air density label
air_density_label = ttk.Label(inner_frame, text="Air Density: ")
air_density_label.grid(row=len(inputs), column=0, columnspan=2, padx=5, pady=2, sticky="w")

# Plotting area
fig, ax = plt.subplots(figsize=(3, 2), dpi=150)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=0, column=2, rowspan=len(inputs) + 1, padx=10, pady=10, sticky="nsew")

# Update button
update_button = ttk.Button(inner_frame, text="Update Plot", command=update_plot)
update_button.grid(row=len(inputs) + 1, column=1, pady=10, sticky="ew")

root.mainloop()
