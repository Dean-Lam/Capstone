from sensors import read_all_sensors
from pumps import run_pump, PUMP, PH_UP, PH_DOWN, NUTRIENT
import time

def control_loop(moisture_target, tds_target, ph_target):
    vol = 1500  # mL

    while True:
        ph, tds, moisture, ph_v, tds_v, moisture_v = read_all_sensors()

        print(f"[INFO] pH: {ph:.2f} ({ph_v:.2f} V) | TDS: {tds:.1f} ppm ({tds_v:.2f} V) | Moisture: {moisture:.1f}% ({moisture_v:.2f} V)")

        if moisture < moisture_target:
            print("[ACTION] Low moisture → Mixing water")
            run_pump(PUMP, 3)
            
            if tds < tds_target:
                print("[ACTION] TDS low → Adding nutrient")
                run_pump(NUTRIENT, 2)
                mix_solution()

            if ph > ph_target + 0.5:
                print("[ACTION] pH too basic → Adding acid")
                run_pump(PH_DOWN, 1)
            elif ph < ph_target - 0.5:
                print("[ACTION] pH too acidic → Adding base")
                run_pump(PH_UP, 1)

        time.sleep(5)

def mix_solution():
    for _ in range(3):
        run_pump(PUMP, 0.3)
        time.sleep(2)
