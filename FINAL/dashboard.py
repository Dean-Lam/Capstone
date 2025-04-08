# Import required libraries
import tkinter as tk  # For GUI window
from tkinter import ttk  # For themed GUI widgets
from sensors import read_all_sensors  # Function to get sensor data
from pumps import run_pump, PUMP_GPIO  # Function and mapping to control pumps

# Define the main dashboard class
class HydroDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Hydroponic System Dashboard")  # Set window title

        self.setup_ui()  # Create and place all widgets on screen
        self.running = True  # Flag to control updates
        self.update_sensor_values()  # Start updating sensor data

    def setup_ui(self):
        # Create a frame (container) to hold the sensor readings table
        table_frame = ttk.Frame(self.root)
        table_frame.pack(pady=10)

        # Add headers for the table: Sensor, Value, and Voltage
        ttk.Label(table_frame, text="Sensor").grid(row=0, column=0, padx=10)
        ttk.Label(table_frame, text="Value").grid(row=0, column=1, padx=10)
        ttk.Label(table_frame, text="Voltage").grid(row=0, column=2, padx=10)

        # Row for pH readings
        ttk.Label(table_frame, text="pH:").grid(row=1, column=0)
        self.ph_value_label = ttk.Label(table_frame, text="...")  # pH value
        self.ph_voltage_label = ttk.Label(table_frame, text="...")  # pH voltage
        self.ph_value_label.grid(row=1, column=1)
        self.ph_voltage_label.grid(row=1, column=2)

        # Row for TDS readings
        ttk.Label(table_frame, text="TDS:").grid(row=2, column=0)
        self.tds_value_label = ttk.Label(table_frame, text="...")  # TDS value
        self.tds_voltage_label = ttk.Label(table_frame, text="...")  # TDS voltage
        self.tds_value_label.grid(row=2, column=1)
        self.tds_voltage_label.grid(row=2, column=2)

        # Row for Moisture readings
        ttk.Label(table_frame, text="Moisture:").grid(row=3, column=0)
        self.moisture_value_label = ttk.Label(table_frame, text="...")  # Moisture %
        self.moisture_voltage_label = ttk.Label(table_frame, text="...")  # Moisture voltage
        self.moisture_value_label.grid(row=3, column=1)
        self.moisture_voltage_label.grid(row=3, column=2)

        # Section for manual pump controls
        ttk.Label(self.root, text="Manual Controls").pack(pady=10)

        # Buttons to manually activate pumps
        ttk.Button(self.root, text="Run Water Pump", command=lambda: run_pump(PUMP_GPIO['water'], 2)).pack(pady=2)
        ttk.Button(self.root, text="Add Nutrient", command=lambda: run_pump(PUMP_GPIO['nutrient'], 1)).pack(pady=2)
        ttk.Button(self.root, text="pH up", command=lambda: run_pump(PUMP_GPIO['ph_up'], 1)).pack(pady=2)
        ttk.Button(self.root, text="pH down", command=lambda: run_pump(PUMP_GPIO['ph_down'], 1)).pack(pady=2)

        # Extra button to quickly "mix" solution (brief water pump run)
        ttk.Button(self.root, text="Mix", command=lambda: run_pump(PUMP_GPIO['water'], 0.1)).pack(pady=5)

        # Exit button to stop the GUI
        ttk.Button(self.root, text="Exit", command=self.stop).pack(pady=10)

    def update_sensor_values(self):
        # Stop updating if flagged
        if not self.running:
            return

        # Get values and voltages from all sensors
        ph, tds, moisture, ph_v, tds_v, moisture_v = read_all_sensors()

        # Update the dashboard labels with new sensor data
        self.ph_value_label.config(text=f"{ph:.2f}")
        self.ph_voltage_label.config(text=f"{ph_v:.2f} V")
        self.tds_value_label.config(text=f"{tds:.1f} ppm")
        self.tds_voltage_label.config(text=f"{tds_v:.2f} V")
        self.moisture_value_label.config(text=f"{moisture:.1f}%")
        self.moisture_voltage_label.config(text=f"{moisture_v:.2f} V")

        # Schedule next update in 2 seconds
        self.root.after(2000, self.update_sensor_values)

    def stop(self):
        # Stop the GUI and exit cleanly
        self.running = False
        self.root.quit()

# Run the dashboard
if __name__ == "__main__":
    root = tk.Tk()  # Create main window
    app = HydroDashboard(root)  # Create dashboard app
    root.mainloop()  # Start GUI loop
