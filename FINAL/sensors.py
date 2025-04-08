# === IMPORTS ===

# Import class for reading analog input from ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

# Import ADS1115 Analog-to-Digital Converter (ADC) class
from adafruit_ads1x15.ads1115 import ADS1115

# Import I2C communication support
import busio

# Import board-specific pin mappings (like SCL, SDA)
import board


# SETUP 

# Define a simple class to name the channels more clearly
# These are just references for the ADS1115 analog input channels A0, A1, A2
class ADS:
    P0 = 0  # Channel A0 (used for pH sensor)
    P1 = 1  # Channel A1 (used for TDS sensor)
    P2 = 2  # Channel A2 (used for Moisture sensor)

# Initialize I2C connection using default pins on Raspberry Pi
i2c = busio.I2C(board.SCL, board.SDA)

# Create an ADS1115 object to interact with the ADC chip
ads = ADS1115(i2c)

# Assign each sensor to a specific analog input channel
ph_channel = AnalogIn(ads, ADS.P0)          # A0 → pH Sensor
moisture_channel = AnalogIn(ads, ADS.P2)    # A2 → Moisture Sensor
tds_channel = AnalogIn(ads, ADS.P1)         # A1 → TDS Sensor


# === CONVERSION FUNCTIONS ===

# Convert voltage from pH sensor into actual pH value using a linear formula
# This formula is based on your experimental calibration
def voltage_to_ph(voltage):
    return (voltage - 0.8962) / 0.1038  # Adjust this if you recalibrate

# Convert voltage from TDS sensor to Total Dissolved Solids (ppm)
# This polynomial equation was fitted from datasheet or testing
def voltage_to_tds(voltage):
    tds_value = (133.42 * voltage**3 - 255.86 * voltage**2 + 857.39 * voltage) * 0.5
    return max(0, tds_value)  # Prevent negative values

# Convert voltage from moisture sensor to percentage (0% = dry, 100% = wet)
def voltage_to_moisture(voltage):
    DRY_VOLTAGE = 3.0  # Voltage expected when soil is dry
    WET_VOLTAGE = 1.0  # Voltage expected when soil is wet

    # Linearly scale the voltage into a percentage range
    moisture_per = (DRY_VOLTAGE - voltage) / (DRY_VOLTAGE - WET_VOLTAGE) * 100
    # Make sure result is between 0 and 100
    moisture_per = max(0, min(100, moisture_per))
    return moisture_per


# SENSOR READ FUNCTIONS 

# Read pH sensor value and the raw voltage
def read_ph():
    voltage = ph_channel.voltage  # Read analog voltage
    ph_value = voltage_to_ph(voltage)  # Convert to pH
    return ph_value, voltage  # Return both for logging/debugging

# Read TDS sensor value and voltage
def read_tds():
    voltage = tds_channel.voltage  # Read analog voltage
    tds = voltage_to_tds(voltage)  # Convert to ppm
    return tds, voltage  # Return both

# Read moisture sensor percentage and voltage
def read_moisture():
    voltage = moisture_channel.voltage  # Read analog voltage
    moisture = voltage_to_moisture(voltage)  # Convert to %
    return moisture, voltage  # Return both


# SENSOR READ FUNCTION

# Read all sensor values and return them at once
def read_all_sensors():
    ph, ph_voltage = read_ph()
    tds, tds_voltage = read_tds()
    moisture, moisture_voltage = read_moisture()
    return ph, tds, moisture, ph_voltage, tds_voltage, moisture_voltage


# TEST CODE TO DISPLAY SENSOR OUTPUT 
# This only runs if the file is executed directly

if __name__ == "__main__":
    # Read sensor values
    ph, tds, moisture, ph_v, tds_v, moisture_v = read_all_sensors()

    # Display results nicely formatted
    print(f"pH Value: {ph:.2f} | Voltage: {ph_v:.2f} V")
    print(f"TDS Value: {tds:.2f} ppm | Voltage: {tds_v:.2f} V")
    print(f"Moisture: {moisture:.2f}% | Voltage: {moisture_v:.2f} V")
