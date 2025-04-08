import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library to control pins
import time  # To use delays for pump timing

# Define GPIO pins connected to each pump or doser
PUMP = 26        # Water circulation pump
PH_UP = 19       # pH increasing pump (adds base)
PH_DOWN = 13     # pH decreasing pump (adds acid)
NUTRIENT = 6     # Nutrient dosing pump

# This dictionary is used for the GUI to refer to the pumps by name
PUMP_GPIO = {
    "water": 26,
    "ph_up": 19,
    "ph_down": 13,
    "nutrient": 6,
}

# Set up each GPIO pin for output (to send signal to relay/pump)
# Also make sure each pump is initially OFF (GPIO.LOW)
for pin in [PUMP, PH_UP, PH_DOWN, NUTRIENT]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Function to run a pump:
# - pin: which GPIO pin the pump is connected to
# - duration_sec: how long to turn the pump ON (in seconds)
def run_pump(pin, duration_sec):
    GPIO.output(pin, GPIO.HIGH)  # Turn the pump ON
    time.sleep(duration_sec)     # Wait for the specified duration
    GPIO.output(pin, GPIO.LOW)   # Turn the pump OFF

# Function to clean up GPIO pins when the program ends
# This ensures all pins are reset and pumps are turned off
def cleanup():
    GPIO.cleanup()
