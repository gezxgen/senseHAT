#!/usr/bin/env python3
from sense_hat import SenseHat
from time import sleep
import datetime

# Initialize Sense HAT
sense = SenseHat()

# Define modes as states
MODES = {
    1: "Binary Clock",
    2: "Date and Time Display",
    3: "Analog Clock",
    4: "Spirit Level",
    5: "Custom Function",
    6: "Internet Data Display"
}

# Current state
current_mode = 1

# Display Mode Function
def display_mode(mode):
    sense.clear()
    if mode == 1:
        display_binary_clock()
    elif mode == 2:
        display_date_and_time()
    elif mode == 3:
        display_analog_clock()
    elif mode == 4:
        display_spirit_level()
    elif mode == 5:
        display_custom_function()
    elif mode == 6:
        display_internet_data()
    else:
        sense.show_message("Invalid Mode")

# Mode Functions (Replace with real implementations)
def display_binary_clock():
    now = datetime.datetime.now()
    binary_hours = bin(now.hour)[2:].zfill(8)
    binary_minutes = bin(now.minute)[2:].zfill(8)
    binary_seconds = bin(now.second)[2:].zfill(8)
    sense.show_message(f"H:{binary_hours} M:{binary_minutes} S:{binary_seconds}", scroll_speed=0.05)

def display_date_and_time():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d %H:%M:%S")
    sense.show_message(date_str, scroll_speed=0.05)

def display_analog_clock():
    sense.show_message("Analog Clock Placeholder", scroll_speed=0.05)

def display_spirit_level():
    orientation = sense.get_orientation()
    pitch = orientation["pitch"]
    roll = orientation["roll"]
    yaw = orientation["yaw"]
    sense.show_message(f"P:{pitch:.1f} R:{roll:.1f} Y:{yaw:.1f}", scroll_speed=0.05)

def display_custom_function():
    sense.show_message("Custom Function Placeholder", scroll_speed=0.05)

def display_internet_data():
    sense.show_message("Internet Data Placeholder", scroll_speed=0.05)

# Joystick event handling
def joystick_moved(event):
    global current_mode
    if event.action == "pressed":
        if event.direction == "right":
            current_mode += 1
            if current_mode > len(MODES):
                current_mode = 1  # Loop back to the first mode
        elif event.direction == "left":
            current_mode -= 1
            if current_mode < 1:
                current_mode = len(MODES)  # Loop to the last mode
        sense.show_message(f"Mode: {MODES[current_mode]}", scroll_speed=0.05)

# Attach the joystick handler
sense.stick.direction_any = joystick_moved

# Main loop
try:
    while True:
        display_mode(current_mode)
        sleep(1)
except KeyboardInterrupt:
    sense.clear()
