from dronekit import connect, Command, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time

# Connect to the Vehicle
print('Connecting to vehicle')
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True)

def arm_and_takeoff(aTargetAltitude):
    print("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)
        
    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude
    
    # Check that vehicle has reached takeoff altitude
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt) 
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


# Initialize the takeoff sequence to 20m
lat = vehicle.location.global_frame.lat
lon = vehicle.location.global_frame.lon
altitude = 60  # Example altitude, adjust as needed
vehicle.commands.clear()  # Clear any existing commands
vehicle.commands.add(Command(
    0,  # Target system
    0,  # Target component
    0,  # Command
    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,  # Frame
    mavutil.mavlink.MAV_CMD_NAV_LOITER_TO_ALT,  # Command
    0,  # Param1
    0,  # Param2
    0,  # Param3
    0,  # Param4
    0,  # Param5
    0,  # Param6
    lat,  # Latitude
    lon,  # Longitude
    altitude  # Altitude
))
vehicle.commands.upload()

# Arm and take off to 40 meters
arm_and_takeoff(40)
print("Take off complete")

# Hover for a bit
time.sleep(10)

print("Now let's Switch to Auto")

# Ensure that mode is properly set before switching
if vehicle.mode.name == 'GUIDED':
    vehicle.mode = VehicleMode("AUTO")
    while vehicle.mode.name != 'AUTO':
        print(" Waiting for AUTO mode...")
        time.sleep(1)
else:
    print("Cannot switch to AUTO mode from current mode:", vehicle.mode.name)

# Hover for a bit in AUTO mode
time.sleep(10)

print("Now let's Switch to Land")
vehicle.mode = VehicleMode("LAND")

# Wait for landing to complete
while vehicle.mode.name != 'LAND':
    print(" Waiting for LAND mode...")
    time.sleep(1)

print("Landing complete")

# Close vehicle object
vehicle.close()