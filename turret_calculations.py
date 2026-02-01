#!/usr/bin/env python3

import math

# Constants
INCHES_PER_FOOT = 12.0
SECONDS_PER_MINUTE = 60.0
GRAVITY_FPS2 = 32.17
HUB_HEIGHT_IN = 72.0

# Values to tinker with
default_shooter_height_in = 17.15
default_wheel_diameter_in = 4.0
default_rpm = 2500.0

rpm_str = input(f"Enter RPMs [empty to use default {default_rpm}]: ")

try:
    rpm = float(rpm_str)
except ValueError:
    rpm = default_rpm

wheel_diameter_str = input(f"Enter wheel diameter in inches [empty to use default {default_wheel_diameter_in}]: ")

try:
    wheel_diameter_in = float(wheel_diameter_str)
except ValueError:
    wheel_diameter_in = default_wheel_diameter_in

shooter_height_str = input(f"Enter shooter height in inches [empty to use default {default_shooter_height_in}]: ")

try:
    shooter_height_in = float(shooter_height_str)
except ValueError:
    shooter_height_in = default_shooter_height_in


class Style():
    RED = '\033[31m'
    GREEN = '\033[32m'
    BLUE = '\033[34m'
    RESET = '\033[0m'

def print_table_header():
    print("Angle\tDist.\tVh\tVv\th\td1\td2\tt1\tt2\tt")

velocity = math.pi * wheel_diameter_in / INCHES_PER_FOOT * rpm / SECONDS_PER_MINUTE / 2

for angle in range(91):
    vh = velocity * math.cos(angle / 180 * math.pi)
    vv = velocity * math.sin(angle / 180 * math.pi)
    h = (vv**2) / (2 * GRAVITY_FPS2)
    t1 = vv / GRAVITY_FPS2
    
    try:
        t2 = math.sqrt(2*((h-(HUB_HEIGHT_IN - shooter_height_in)/12)/GRAVITY_FPS2))
    except ValueError:
        # Catch exceptions where trying to take the square root of a negative number
        t2 = 0
    
    t = t1 + t2
    d1 = t1 * vh
    d2 = t2 * vh

    # Distance is set to 0 for calculations that generate an error, such as height too low
    # to reach hub
    distance = d1 + d2 if t2 > 0 else 0.0
    
    # h is peak height above shooter, not measured from the floor
    # Angle is measured from horizontal

    # Reprint the table header every so often to make it easier to view the data
    if angle % 10 == 0:
        print_table_header()

    background = Style.RED if math.isclose(distance, 0, abs_tol=0.0001) else Style.GREEN
    print(f"{background}{angle}\t{distance:.3f}\t{vh:.3f}\t{vv:.3f}\t{h:.3f}\t{d1:.3f}\t{d2:.3f}\t{t1:.3f}\t{t2:.3f}\t{t:.3f}{Style.RESET}")

print(f"\n\nWheel Diameter:{wheel_diameter_in} inches\nShooter Height: {shooter_height_in} inches\nRPM: {rpm}\nVelocity: {velocity:.3f} fps\n\n")
