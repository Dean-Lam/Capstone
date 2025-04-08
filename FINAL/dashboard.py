import tkinter as tk
from tkinter import ttk
from sensors import read_all_sensors
from pumps import run_pump, PUMP_GPIO

class HydroDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Hydroponic System Dashboard")

        self.setup_ui()
        self.running = True
        self.update_sensor_values()

    def setup_ui(self):
        # Create a frame for the sensor table
        table_frame = ttk.Frame(self.root)
        table_frame.pack(pady=10)

        # Table headers
        ttk.Label(table_frame, text="Sensor").grid(row=0, column=0, padx=10)
        ttk.Label(table_frame, text="Value").grid(row=0, column=1, padx=10)
        ttk.Label(table_frame, text="Voltage").grid(row=0, column=2, padx=10)

        # Sensor labels
        ttk.Label(table_frame, text="pH:").grid(row=1, column=0)
        self.ph_value_label = ttk.Label(table_frame, text="...")
        self.ph_voltage_label = ttk.Label(table_frame, text="...")
        self.ph_value_label.grid(row=1, column=1)
        self.ph_voltage_label.grid(row=1, column=2)

        ttk.Label(table_frame, text="TDS:").grid(row=2, column=0)
        self.tds_value_label = ttk.Label(table_frame, text="...")
        self.tds_voltage_label = ttk.Label(table_frame, text="...")
        self.tds_value_label.grid(row=2, column=1)
        self.tds_voltage_label.grid(row=2, column=2)

        ttk.Label(table_frame, text="Moisture:").grid(row=3, column=0)
        self.moisture_value_label = ttk.Label(table_frame, text="...")
        self.moisture_voltage_label = ttk.Label(table_frame, text="...")
        self.moisture_value_label.grid(row=3, column=1)
        self.moisture_voltage_label.grid(row=3, column=2)

        # Manual control buttons
        ttk.Label(self.root, text="Manual Controls").pack(pady=10)

        ttk.Button(self.root, text="Run Water Pump", command=lambda: run_pump(PUMP_GPIO['water'], 2)).pack(pady=2)
        ttk.Button(self.root, text="Add Nutrient", command=lambda: run_pump(PUMP_GPIO['nutrient'], 1)).pack(pady=2)
        ttk.Button(self.root, text="pH up", command=lambda: run_pump(PUMP_GPIO['ph_up'], 1)).pack(pady=2)
        ttk.Button(self.root, text="pH down", command=lambda: run_pump(PUMP_GPIO['ph_down'], 1)).pack(pady=2)

        # Mix Button
        ttk.Button(self.root, text="Mix", command=lambda: run_pump(PUMP_GPIO['water'], 0.1)).pack(pady=5)

        # Exit Button
        ttk.Button(self.root, text="Exit", command=self.stop).pack(pady=10)

    def update_sensor_values(self):
        if not self.running:
            return

        ph, tds, moisture, ph_v, tds_v, moisture_v = read_all_sensors()

        self.ph_value_label.config(text=f"{ph:.2f}")
        self.ph_voltage_label.config(text=f"{ph_v:.2f} V")
        self.tds_value_label.config(text=f"{tds:.1f} ppm")
        self.tds_voltage_label.config(text=f"{tds_v:.2f} V")
        self.moisture_value_label.config(text=f"{moisture:.1f}%")
        self.moisture_voltage_label.config(text=f"{moisture_v:.2f} V")

        self.root.after(2000, self.update_sensor_values)

    def stop(self):
        self.running = False
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = HydroDashboard(root)
    root.mainloop()
