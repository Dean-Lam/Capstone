# Import functions to read sensor data and control pumps
from sensors import read_all_sensors
from pumps import run_pump, PUMP, PH_UP, PH_DOWN, NUTRIENT
import time

# Main function to continuously monitor and control the system
def control_loop(moisture_target, tds_target, ph_target):
    vol = 1500  # total water volume in mL (used for calculations if needed)

    while True:
        # Read current values from all sensors
        ph, tds, moisture, ph_v, tds_v, moisture_v = read_all_sensors()

        # Print the current readings to the console for monitoring
        print(f"[INFO] pH: {ph:.2f} ({ph_v:.2f} V) | TDS: {tds:.1f} ppm ({tds_v:.2f} V) | Moisture: {moisture:.1f}% ({moisture_v:.2f} V)")

        # Check if moisture is too low
        if moisture < moisture_target:
            print("[ACTION] Low moisture → Mixing water")
            run_pump(PUMP, 3)  # Run water pump for 3 seconds

            # Check if nutrients need to be added
            if tds < tds_target:
                print("[ACTION] TDS low → Adding nutrient")
                run_pump(NUTRIENT, 2)  # Run nutrient pump for 2 seconds
                mix_solution()  # Mix the solution to evenly distribute the nutrients

            # Check if pH needs to be adjusted
            if ph > ph_target + 0.5:
                print("[ACTION] pH too basic → Adding acid")
                run_pump(PH_DOWN, 1)  # Run pH down pump for 1 second
            elif ph < ph_target - 0.5:
                print("[ACTION] pH too acidic → Adding base")
                run_pump(PH_UP, 1)  # Run pH up pump for 1 second

        # Wait for 5 seconds before the next reading
        time.sleep(5)

# Function to mix the solution by cycling the water pump
def mix_solution():
    for _ in range(3):  # Repeat the mixing cycle 3 times
        run_pump(PUMP, 0.3)  # Run pump for 0.3 seconds
        time.sleep(2)  # Wait 2 seconds before repeating
