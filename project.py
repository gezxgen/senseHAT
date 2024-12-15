from math import cos, sin, radians
from datetime import datetime
from sense_hat import SenseHat
from time import sleep
from requests import get
from re import search
from bs4 import BeautifulSoup


def temperature(sense):
    sense.show_letter("5")


def internet(sense):
    response = get("https://www.instagram.com/kevin_amm1/")
    soup = BeautifulSoup(response.text, "html.parser")
    match = search(r"(\d+)\sFollowers,\s(\d+)\sFollowing", str(soup))

    if match and match.group(1) and match.group(2):
        sense.show_message(f"Followers: {match.group(1)}, Following: {match.group(2)}")


def water_scale(sense):
    # Get raw acceleration data from the Sense HAT
    pixels = [(0, 0, 0)] * 64
    acceleration = sense.get_accelerometer_raw()
    x = int(min(max((1 - acceleration["x"]) * 4, 0), 6))
    y = int(min(max((1 - acceleration["y"]) * 4, 0), 6))

    # Light up the corresponding 2x2 block
    for i in range(2):
        for j in range(2):
            pixels[int((y + i) * 8 + x + j)] = (255, 255, 255)  # Set pixel to white

    sense.set_pixels(pixels)


def binary_clock(sense):
    sense.clear()
    now = datetime.now()
    pixels = [[0, 0, 0] for _ in range(64)]

    # Convert time to binary
    binary_hours = bin(now.hour)[2:].zfill(8)
    binary_minutes = bin(now.minute)[2:].zfill(8)
    binary_seconds = bin(now.second)[2:].zfill(8)

    # Define binary representation
    for i in range(8):
        # Hours (columns 0-1)
        if binary_hours[7 - i] == '1':
            pixels[(i + 2) * 8] = [0, 0, 255]  # Blue
            pixels[(i + 2) * 8 + 1] = [0, 0, 255]

        # Minutes (columns 3-4)
        if binary_minutes[7 - i] == '1':
            pixels[(i + 2) * 8 + 3] = [255, 0, 0]  # Red
            pixels[(i + 2) * 8 + 4] = [255, 0, 0]

        # Seconds (columns 6-7)
        if binary_seconds[7 - i] == '1':
            pixels[(i + 2) * 8 + 6] = [0, 255, 0]  # Green
            pixels[(i + 2) * 8 + 7] = [0, 255, 0]

    sense.set_pixels(pixels)


def binary_date(sense):
    sense.clear()
    now = datetime.now()
    pixels = [[0, 0, 0] for _ in range(64)]

    # Convert date and time components to binary
    year_binary = bin(now.year)[2:].zfill(16)
    month_binary = bin(now.month)[2:].zfill(8)
    day_binary = bin(now.day)[2:].zfill(8)
    weekday_binary = bin(now.weekday() + 1)[2:].zfill(8)
    hours_binary = bin(now.hour)[2:].zfill(8)
    minutes_binary = bin(now.minute)[2:].zfill(8)
    seconds_binary = bin(now.second)[2:].zfill(8)

    for i in range(8):
        # MSBs (bottom left)
        if year_binary[i] == '1':  # MSB part (first 8 bits)
            pixels[(7 - i) * 8] = [128, 0, 128]  # Purple (MSB column, placed bottom to top)

        # LSBs (top right, reversed)
        if year_binary[15 - i] == '1':  # LSB part (last 8 bits)
            pixels[i * 8 + 1] = [128, 0, 128]  # Purple (LSB column, placed top to bottom)

        # Month (column 2) - Cyan
        if month_binary[7 - i] == '1':
            pixels[i * 8 + 2] = [0, 255, 255]  # Cyan

        # Day (column 3) - Yellow
        if day_binary[7 - i] == '1':
            pixels[i * 8 + 3] = [255, 255, 0]  # Yellow

        # Weekday (column 4) - Orange
        if weekday_binary[7 - i] == '1':
            pixels[i * 8 + 4] = [255, 165, 0]  # Orange

        # Hours (column 5) - Blue
        if hours_binary[7 - i] == '1':
            pixels[i * 8 + 5] = [255, 0, 0]  # Blue

        # Minutes (column 6) - Red
        if minutes_binary[7 - i] == '1':
            pixels[i * 8 + 6] = [0, 0, 255]  # Red

        # Seconds (column 7) - Green
        if seconds_binary[7 - i] == '1':
            pixels[i * 8 + 7] = [0, 255, 0]  # Green

    sense.set_pixels(pixels)


def analog_clock(sense):
    # Get the current time
    now = datetime.now()
    seconds = now.second
    minutes = now.minute
    hours = now.hour

    # Clear the screen
    sense.clear()

    # Center of the clock face
    center = (3, 3)

    # Define the colors for the clock hands
    green = [0, 255, 0]  # Seconds hand (green)
    red = [255, 0, 0]  # Minutes hand (red)
    blue = [0, 0, 255]  # Hours hand (blue)

    # Function to draw a hand from the center to the edge
    def draw_hand(angle, length, color):
        for i in range(1, length + 1):
            # Calculate the x, y position for each point along the hand
            x = center[0] + int(cos(radians(angle)) * i)
            y = center[1] + int(sin(radians(angle)) * i)

            # Clamp the coordinates to be within the 0-7 range
            x = max(0, min(7, x))  # Ensure x is between 0 and 7
            y = max(0, min(7, y))  # Ensure y is between 0 and 7

            # Set each pixel for the hand
            sense.set_pixel(x, y, color)

    # Draw the seconds hand (green) with a length of 5
    second_angle = (seconds % 60) * 6  # 360 degrees / 60 seconds = 6 degrees per second
    draw_hand(second_angle, 5, green)  # Seconds hand length is 5

    # Draw the minutes hand (red) with a length of 4
    minute_angle = (minutes % 60) * 6  # 360 degrees / 60 minutes = 6 degrees per minute
    draw_hand(minute_angle, 4, red)  # Minutes hand length is 4

    # Draw the hours hand (blue) with a length of 3
    # The hour hand should move slightly depending on the minute as well
    hour_angle = ((hours % 12) + minutes / 60) * 30  # 360 degrees / 12 hours = 30 degrees per hour
    draw_hand(hour_angle, 3, blue)  # Hours hand length is 3


# Joystick event handling
def joystick_moved(event, current_mode, total_modes):
    # if nothing was pressed, just return the given value
    if event.action != "pressed":
        return current_mode

    # if pressed to right, increment
    if event.direction == "right":
        return (current_mode % total_modes) + 1

    # if pressed to left, decrement
    if event.direction == "left":
        return (current_mode - 2) % total_modes + 1


def main():
    # Initialize Sense HAT
    sense = SenseHat()

    # Current state
    current_mode = 1
    total_modes = 6

    # Main loop
    try:
        while True:
            # Display the current mode based on match-case
            match current_mode:
                case 1:
                    binary_clock(sense)
                case 2:
                    binary_date(sense)
                case 3:
                    analog_clock(sense)
                case 4:
                    water_scale(sense)
                case 5:
                    temperature(sense)
                case 6:
                    internet(sense)

            # Check for joystick events
            for event in sense.stick.get_events():
                current_mode = joystick_moved(event, current_mode, total_modes)

            sleep(0.1)
    except KeyboardInterrupt:
        sense.clear()


if __name__ == "__main__":
    main()
