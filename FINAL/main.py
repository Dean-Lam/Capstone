from control import control_loop  # Import the main automation logic
from pumps import cleanup         # Import a function to clean up the GPIO pins (turn things off)

try:
    # Start the control loop with desired target values:
    # - moisture_target: trigger if soil is drier than 50%
    # - tds_target: trigger if nutrients are below 500 ppm
    # - ph_target: trigger if pH is not close to 6
    control_loop(moisture_target=50, tds_target=500, ph_target=6)

except KeyboardInterrupt:
    # If the user presses CTRL+C to stop the program...
    print("Shutting down safely...")

    # Turn off pumps and clean up GPIO pins so nothing is left running
    cleanup()
