# sumo_ns3_bridge.py
import traci
import json
import time
import os

traci.init(8813)  # SUMO must be started in TraCI mode on this port

uwb_log = []
uwb_log_file = "uwb_events.json"

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    time_now = traci.simulation.getTime()

    vehicle_data = []
    pedestrian_data = []

    # Get all vehicle positions
    for vid in traci.vehicle.getIDList():
        x, y = traci.vehicle.getPosition(vid)
        vehicle_data.append({"id": vid, "x": x, "y": y})

    # Get pedestrian position (assume only 1)
    for pid in traci.person.getIDList():
        x, y = traci.person.getPosition(pid)
        pedestrian_data.append({"id": pid, "x": x, "y": y})

    # Only if 3 vehicles and 1 pedestrian are present
    if len(vehicle_data) == 3 and len(pedestrian_data) == 1:
        uwb_log.append({
            "time": time_now,
            "vehicles": vehicle_data,
            "pedestrian": pedestrian_data[0]
        })

    time.sleep(0.1)

traci.close()

# Save to JSON
with open(uwb_log_file, "w") as f:
    json.dump(uwb_log, f, indent=2)

print(f"[✓] UWB Events saved to {uwb_log_file}")
