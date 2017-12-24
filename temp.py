# Import Libraries
import os
import glob
import time

# Initial code from:
# https://thepihut.com/blogs/raspberry-pi-tutorials/
# 18095732-sensors-temperature-with-the-1-wire-interface-and-the-ds18b20

# Initialize the GPIO Pins
os.system('modprobe w1-gpio')  # Turns on the GPIO module
os.system('modprobe w1-therm')  # Turns on the Temperature module

# Finds the correct device file that holds the temperature data
BASE_DIR = '/sys/bus/w1/devices/'

# A function that reads the sensors data
def read_temp_raw(file):
    f = open(file, 'r')  # Opens the temperature device file
    lines = f.readlines()  # Returns the text
    f.close()
    return lines


# Convert the value of the sensor into a temperature
def read_temp(file):
    lines = read_temp_raw(file)  # Read the temperature 'device file'

    # While the first line does not contain 'YES', wait for 0.2s
    # and then read the device file again.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()

    # Look for the position of the '=' in the second line of the
    # device file.
    equals_pos = lines[1].find('t=')

    # If the '=' is found, convert the rest of the line after the
    # '=' into degrees Celsius, then degrees Fahrenheit
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f


def find_files():

    device_folders = glob.glob(BASE_DIR + '28*')[0]

    for folder in device_folders:
        device_file = folder + '/w1_slave'
        current_time = str(time.strftime('%X %x %Z'))
        temp_c, temp_f = read_temp(device_file)
        print(str(folder) + current_time + str(temp_c) + ' C, ' + str(temp_f) + ' F')


# Print out the temperature until the program is stopped.
while True:
    find_files()
    time.sleep(1)
