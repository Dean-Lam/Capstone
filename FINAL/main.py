from control import control_loop
from pumps import cleanup

try:
    # Set your thresholds here
    control_loop(moisture_target=50, tds_target=500, ph_target=6)

except KeyboardInterrupt:
    print("Shutting down safely...")
    cleanup()
