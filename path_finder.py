# Need to be changed based on drone specs
SAFTEY_LIMIT = 15 #Percent of battery when you need to return
CHARGE_TIME = 1800 #In seconds
SPEED = 10 #m/s
PW_CONSUPTION = 400 #Power consumption in watts
BATTERY_VOLT = 14.8 #Voltage of battery
BATTERY_CAP = 6 #Battery capacity in Ah


# Lists to hold x and y boundary points
x_bounds = []
y_bounds = []



# List for specs of drone
spec_values = []

def getBoundary():
    # Prompts the user for 4 boundary points
    cnt = 1
    while cnt < 5:
        point = input("Enter boundary point {} in meters as x, y: ".format(cnt))
        point = point.split(', ')
        # Trys to convert input to integers and add to boundry lists
        try:
            x = int(point[0])
            y = int(point[1])

            x_bounds.append(x)
            y_bounds.append(y)

            cnt += 1
        # If non integer is entered
        except(ValueError):
            print("Invalid format")
        # If 2 integers are not given
        except(IndexError):
            print("Either x or y was not given")

def specs():
    speed = int(input("Enter the speed of the drone (only enter numbers): "))
    units = input("What is the units for the speed? (m/s, mph, or km/h): ")
    valid = False
    # Converts speed to km/h
    while valid == False:
        if(units.lower() == "m/s"):
            speed = speed * 3.6
            valid = True
        elif(units.lower() == "mph"):
            speed = speed * 1.60934
            valid = True
        elif(units.lower() == 'km/h'):
            valid = True
        else:
            print("Incompatible units, make sure units are on list of approved units")

    weight = input("Enter weight of drone: ")
    battery_cap = input("Enter the max charge value for the battery: ")
    battery_drain = input("Enter battery drain rate: ")

    spec_values.append(speed)
    spec_values.append(weight)
    spec_values.append(battery_cap)
    spec_values.append(battery_drain)




def main():
    # Gather information from user
    getBoundary()

    startX = x_bounds[0]
    endX = x_bounds[2]
    startY = y_bounds[0]
    endY = y_bounds[2]

    #Calculate battery capacity in W/h
    battery_cap = BATTERY_CAP * BATTERY_VOLT

    #Find time to fly 1m
    time = 1/SPEED

    #Find energy consumed(Wh)
    consumed = PW_CONSUPTION * (time/3600) #Converts time from seconds to hours 

    #Calculate percentage of the battery used to move 1 meter at 10m/s
    percentage = (consumed/battery_cap)*100
    
    current_percent = 100

    x_max = x_bounds[1]
    y_max = y_bounds[2]

    
    #Calculate battery percent used to fly row
    percent_per_row = 0
    time_per_row = 0
    for x in range(x_max):
        percent_per_row += percentage
        time_per_row += 0.1
    print("Percent cost per row: {}".format(percent_per_row))

    num_charges = 0
    fly_time = 0

    max_return_cost = y_max * percentage # Calculates the max battery cost to fly back to home base 

    current_y = y_bounds[0] + 1
    # While the drone is still in the bounds of the field
    while current_y <= y_max:
        print("Current Y: {}".format(current_y))
        # If the current battery percent is at a safe level, complete down and back while adding time to flight time
        if((current_percent - 2*percent_per_row) > (max_return_cost+SAFTEY_LIMIT)):
            current_percent -= 2*percent_per_row
            fly_time += 2*time_per_row
        #Otherwise
        else:
            print("Cannot safely complete down and back. Heading back to home base.")
            # Calculate return battery consumption and time to fly back to home base
            return_cost = current_y * percentage
            return_time = current_y * 0.1
            current_percent -= return_cost
            fly_time += return_time
            print("Percent before charge: {}".format(current_percent))
            print("Charging...")
            fly_time += CHARGE_TIME
            num_charges += 1
            current_percent = 100 #Reset charge to 100%
            print("Fully Charged")
            #Calculate battery cost and time to return to next row to fly over
            resume_cost = (current_y + 1) * percentage
            resume_time = (current_y + 1) * 0.1
            current_percent -= resume_cost
            fly_time += resume_time
            
        #Increase the y value by 2 to represnt fly the length of one row and returning on the next row, covering 2 rows in total
        current_y += 2
        print("Current Percent: {}".format(current_percent))

    print("\nFlight Time: {} hours\nNumber of charges: {}".format(fly_time/3600, num_charges))    

if __name__=="__main__":
    main()

