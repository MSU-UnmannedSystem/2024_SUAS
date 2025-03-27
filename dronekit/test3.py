from __future__ import print_function
import time
import sys
import os
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command
import argparse
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from field_mapping.scan import scanner

parser = argparse.ArgumentParser(description="Square mission with mode switching and mapping demonstration")
parser.add_argument("--connect", help="Vehicle connection target string")
args = parser.parse_args()

connection_string = args.connect if args.connect else "udp:172.17.208.1:14550"

HOME_POSITION = (53.280707, -9.031534, 0)
SQUARE_SIZE = 0.001
SURVEY_STRIP_WIDTH = 0.002
FLIGHT_ALTITUDE = 20

leScan = scanner(500,500,100)

def calculate_s_pattern_waypoints(start_point, field_coordinates):
    if len(field_coordinates) != 4:
        raise ValueError("Field must be defined by 4 coordinates")
    
    min_lat = min(coord[0] for coord in field_coordinates)
    max_lat = max(coord[0] for coord in field_coordinates)
    min_lon = min(coord[1] for coord in field_coordinates)
    max_lon = max(coord[1] for coord in field_coordinates)
    
    survey_waypoints = []
    current_lat = min_lat
    current_lon = min_lon
    direction = 1
    
    while (current_lat <= max_lat and current_lon <= max_lon):
        survey_waypoints.append((current_lat, current_lon, 30))
        current_lat += (SURVEY_STRIP_WIDTH*direction)
        if(current_lat==max_lat):
            direction *= -1 
            current_lon += SURVEY_STRIP_WIDTH
        survey_waypoints.append((current_lat, current_lon, 30))
    
    return survey_waypoints

def scan_field(field_coordinates):
    survey_waypoints = calculate_s_pattern_waypoints(
        (vehicle.location.global_relative_frame.lat, 
         vehicle.location.global_relative_frame.lon), 
        field_coordinates
    )
    
    for wp in survey_waypoints:
        target_point = LocationGlobalRelative(wp[0], wp[1], wp[2])
        vehicle.simple_goto(target_point)
        time.sleep(15)

def calculate_waypoints():
    return [
        (HOME_POSITION[0] + SQUARE_SIZE, HOME_POSITION[1], FLIGHT_ALTITUDE),
        (HOME_POSITION[0] + SQUARE_SIZE, HOME_POSITION[1] + SQUARE_SIZE, FLIGHT_ALTITUDE),
        (HOME_POSITION[0], HOME_POSITION[1] + SQUARE_SIZE, FLIGHT_ALTITUDE),
        (HOME_POSITION[0], HOME_POSITION[1], FLIGHT_ALTITUDE)
    ]

def arm_and_takeoff(aTargetAltitude):
    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    timeout = time.time() + 60
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)
    if not vehicle.armed:
        print("Failed to arm vehicle.")
        return

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)

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
    
    cmds.add(Command(
        0, 0, 0, 3, 22, 0, 0, 0, 0, 0, 0, 0, 0, FLIGHT_ALTITUDE
    ))
    
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

print(f"Connecting to vehicle: {connection_string}")
vehicle = connect(connection_string, wait_ready=True, heartbeat_timeout=60)

clear_mission()
upload_mission()

arm_and_takeoff(FLIGHT_ALTITUDE)

print("\nStarting square mission in AUTO mode")
vehicle.mode = VehicleMode("AUTO")
time.sleep(2)
print_status()

wait_for_waypoint(vehicle, 2)
print_status()

print("\n--- INTERRUPTING MISSION ---")
vehicle.mode = VehicleMode("GUIDED")
while vehicle.mode.name != "GUIDED":
    time.sleep(0.5)
print_status()

detour_point = LocationGlobalRelative(
    vehicle.location.global_relative_frame.lat + SQUARE_SIZE/2,
    vehicle.location.global_relative_frame.lon + SQUARE_SIZE/2,
    FLIGHT_ALTITUDE
)
print(f"\nGoing to detour point: {detour_point}")
vehicle.simple_goto(detour_point, groundspeed=5)

time.sleep(15)
print("\nDetour complete")
print_status()

print("\n--- RESUMING MISSION ---")
vehicle.mode = VehicleMode("AUTO")

print("\n--- INTERRUPTING MISSION ---")
vehicle.mode = VehicleMode("GUIDED")
while vehicle.mode.name != "GUIDED":
    time.sleep(0.5)
print_status()

field_coordinates = [
    (vehicle.location.global_relative_frame.lat - SQUARE_SIZE, vehicle.location.global_relative_frame.lon - SQUARE_SIZE, FLIGHT_ALTITUDE),
    (vehicle.location.global_relative_frame.lat - SQUARE_SIZE, vehicle.location.global_relative_frame.lon + SQUARE_SIZE, FLIGHT_ALTITUDE),
    (vehicle.location.global_relative_frame.lat + SQUARE_SIZE, vehicle.location.global_relative_frame.lon + SQUARE_SIZE, FLIGHT_ALTITUDE),
    (vehicle.location.global_relative_frame.lat + SQUARE_SIZE, vehicle.location.global_relative_frame.lon - SQUARE_SIZE, FLIGHT_ALTITUDE)
]

scan_field(field_coordinates)

vehicle.mode = VehicleMode("RTL")
time.sleep(10)

vehicle.close()