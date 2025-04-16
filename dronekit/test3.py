
from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command
import argparse

# Set up option parsing
parser = argparse.ArgumentParser(description="Square mission with mode switching demonstration")
parser.add_argument("--connect", help="Vehicle connection target string")
args = parser.parse_args()

connection_string = "/dev/ttyAMA0"

# Home position (from SITL command)
HOME_POSITION = (53.280707, -9.031534, 0)
# HOME_POSITION = (53.2807071, -9.0315358, 0)
SQUARE_SIZE = 0.001  # Degrees (~111 meters per degree)
FLIGHT_ALTITUDE = 20  # Meters

def calculate_waypoints():
    """Generate square waypoints based on home position"""
    return [
        (HOME_POSITION[0] + SQUARE_SIZE, HOME_POSITION[1], FLIGHT_ALTITUDE),
        (HOME_POSITION[0] + SQUARE_SIZE, HOME_POSITION[1] + SQUARE_SIZE, FLIGHT_ALTITUDE),
        (HOME_POSITION[0], HOME_POSITION[1] + SQUARE_SIZE, FLIGHT_ALTITUDE),
        (HOME_POSITION[0], HOME_POSITION[1], FLIGHT_ALTITUDE)  # Close the square
    ]

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    timeout = time.time() + 60  # 60 seconds timeout
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)
    if not vehicle.armed:
        print("Failed to arm vehicle.")
        return
    timeout = time.time() + 15  # 30 seconds timeout
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)
    if not vehicle.armed:
        print("Failed to arm vehicle.")
        return

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

def clear_mission():
    cmds = vehicle.commands
    cmds.clear()
    vehicle.flush()

def upload_mission():
    print("Uploading square mission")
    cmds = vehicle.commands
    cmds.clear()
    
    # Add takeoff command
    cmds.add(Command(
        0, 0, 0, 3, 22, 0, 0, 0, 0, 0, 0, 0, 0, FLIGHT_ALTITUDE
    ))
    
    # Add square waypoints
    waypoints = calculate_waypoints()
    seq_num = 1
    for wp in waypoints:
        cmds.add(Command(
            seq_num, 0, 0, 3, 16, 0, 1,
            0, 0, 0, 0, wp[0], wp[1], wp[2]
        ))
        seq_num += 1
    
    cmds.upload()
    print(f"Uploaded {len(waypoints)} waypoints")


def wait_for_waypoint(vehicle, target_seq):
    print(f"Waiting for waypoint {target_seq}")
    while True:
        next_wp = vehicle.commands.next
        print(f" Current WP: {next_wp-1}/{len(vehicle.commands)-1}", end='\r')
        if next_wp > target_seq:
            print(f"\nReached waypoint {target_seq}")
            break
        time.sleep(1)

def print_status():
    print(f"\n[STATUS] Mode: {vehicle.mode.name}")
    print(f" Position: {vehicle.location.global_relative_frame}")
    print(f" Altitude: {vehicle.location.global_relative_frame.alt:.1f}m")

# Main execution
print(f"Connecting to vehicle: {connection_string}")
vehicle = connect(connection_string, wait_ready=True, heartbeat_timeout=60, baud=57600)

# Setup mission
# clear_mission()
# upload_mission()

# Arm and takeoff
# arm_and_takeoff(FLIGHT_ALTITUDE)

# Start mission
# print("\nStarting square mission in AUTO mode")
# vehicle.mode = VehicleMode("AUTO")
# time.sleep(2)
# print_status()

wait_for_waypoint(vehicle, 2)
print_status()

# Switch to GUIDED mode
print("\n--- INTERRUPTING MISSION ---")
vehicle.mode = VehicleMode("GUIDED")
while vehicle.mode.name != "GUIDED":
    time.sleep(0.5)
print_status()

# Execute custom command
detour_point = LocationGlobalRelative(
    vehicle.location.global_relative_frame.lat + SQUARE_SIZE/2,
    vehicle.location.global_relative_frame.lon + SQUARE_SIZE/2,
    FLIGHT_ALTITUDE
)
print(f"\nGoing to detour point: {detour_point}")
vehicle.simple_goto(detour_point, groundspeed=5)

# Wait to reach detour point
time.sleep(15)
print("\nDetour complete")
print_status()

# Resume mission
print("\n--- RESUMING MISSION ---")
vehicle.mode = VehicleMode("AUTO")
while vehicle.mode.name != "AUTO":
    time.sleep(0.5)
print_status()

# Wait for mission completion
wait_for_waypoint(vehicle, len(vehicle.commands)-1)
print("\nMission complete")

# Return to launch
print("\nReturning to launch")
vehicle.mode = VehicleMode("RTL")
time.sleep(10)
print_status()

print("\nClosing connection")
vehicle.close()
