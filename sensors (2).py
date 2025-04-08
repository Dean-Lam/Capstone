from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1115 import ADS1115
import busio
import board

class ADS:
    P0 = 0
    P1 = 1
    P2 = 2
    
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS1115(i2c)

# Assign channels
ph_channel = AnalogIn(ads, ADS.P0)
moisture_channel = AnalogIn(ads, ADS.P2)
tds_channel = AnalogIn(ads, ADS.P1)

def voltage_to_ph(voltage):
    return (voltage - 0.8962)/0.1038

def voltage_to_tds(voltage):
   tds_value = (133.42 * voltage**3 -255.86 * voltage ** 2 + 857.39 * voltage) * 0.5
   return max(0, tds_value)

def voltage_to_moisture(voltage):
    DRY_VOLTAGE = 3.0
    WET_VOLTAGE = 1.0

    moisture_per = (DRY_VOLTAGE - voltage) / (DRY_VOLTAGE - WET_VOLTAGE) * 100
    moisture_per = max(0, min(100, moisture_per))
    return moisture_per

#Read values

def read_ph():
    voltage = ph_channel.voltage
    ph_value = voltage_to_ph(voltage)
    return ph_value, voltage

def read_tds():
    voltage = tds_channel.voltage
    tds = voltage_to_tds(voltage)
    return tds, voltage

def read_moisture():
    voltage = moisture_channel.voltage
    moisture = voltage_to_moisture(voltage)
    return moisture, voltage

def read_all_sensors():
    ph, ph_voltage = read_ph()
    tds, tds_voltage = read_tds()
    moisture, moisture_voltage = read_moisture()
    return ph, tds, moisture, ph_voltage, tds_voltage, moisture_voltage

if __name__ == "__main__":
    ph, tds, moisture, ph_v, tds_v, moisture_v = read_all_sensors()
    print(f"pH Value: {ph:.2f} | Voltage: {ph_v:.2f} V")
    print(f"TDS Value: {tds:.2f} ppm | Voltage: {tds_v:.2f} V")
    print(f"Moisture: {moisture:.2f}% | Voltage: {moisture_v:.2f} V")





