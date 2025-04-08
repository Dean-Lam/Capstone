import RPi.GPIO as GPIO
import time

# Define GPIO pins
PUMP = 26
PH_UP = 19
PH_DOWN = 13
NUTRIENT = 6

#for GUI
PUMP_GPIO={
    "water": 26,
    "ph_up": 19,
    "ph_down": 13,
    "nutrient": 6,
}

#pin allocation
for pin in [PUMP, PH_UP, PH_DOWN, NUTRIENT]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def run_pump(pin, duration_sec):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(duration_sec)
    GPIO.output(pin, GPIO.LOW)

def cleanup():
    GPIO.cleanup()
