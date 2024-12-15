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

    # Convert time to binary
    hours, minutes = bin(now.hour)[2:].zfill(8), bin(now.minute)[2:].zfill(8)
    seconds, pixels = bin(now.second)[2:].zfill(8), [[0, 0, 0] for _ in range(64)]

    # Define binary representation
    for i in range(8):
        # Hours (columns 0-1)
        if hours[7 - i] == '1':
            pixels[(i + 2) * 8] = [0, 0, 255]  # Blue
            pixels[(i + 2) * 8 + 1] = [0, 0, 255]

        # Minutes (columns 3-4)
        if minutes[7 - i] == '1':
            pixels[(i + 2) * 8 + 3] = [255, 0, 0]  # Red
            pixels[(i + 2) * 8 + 4] = [255, 0, 0]

        # Seconds (columns 6-7)
        if seconds[7 - i] == '1':
            pixels[(i + 2) * 8 + 6] = [0, 255, 0]  # Green
            pixels[(i + 2) * 8 + 7] = [0, 255, 0]

    sense.set_pixels(pixels)


def binary_date(sense):
    sense.clear()
    now = datetime.now()

    # Convert date and time components to binary
    year, month,  = bin(now.year)[2:].zfill(16), bin(now.month)[2:].zfill(8)
    day, weekday = bin(now.day)[2:].zfill(8), bin(now.weekday() + 1)[2:].zfill(8)
    hours, minutes = bin(now.hour)[2:].zfill(8), bin(now.minute)[2:].zfill(8)
    seconds, pixels = bin(now.second)[2:].zfill(8), [[0, 0, 0] for _ in range(64)]

    for i in range(8):
        # MSBs (bottom left) first, then LSBs (top right, reversed)
        if year[i] == '1':
            pixels[(7 - i) * 8] = [128, 0, 128]
        if year[15 - i] == '1':
            pixels[i * 8 + 1] = [128, 0, 128]

        # Month (column 2) - Cyan
        if month[7 - i] == '1':
            pixels[i * 8 + 2] = [0, 255, 255]

        # Day (column 3) - Yellow
        if day[7 - i] == '1':
            pixels[i * 8 + 3] = [255, 255, 0]

        # Weekday (column 4) - Orange
        if weekday[7 - i] == '1':
            pixels[i * 8 + 4] = [255, 165, 0]

        # Hours (column 5) - Blue
        if hours[7 - i] == '1':
            pixels[i * 8 + 5] = [255, 0, 0]

        # Minutes (column 6) - Red
        if minutes[7 - i] == '1':
            pixels[i * 8 + 6] = [0, 0, 255]

        # Seconds (column 7) - Green
        if seconds[7 - i] == '1':
            pixels[i * 8 + 7] = [0, 255, 0]

    sense.set_pixels(pixels)


def analog_clock(sense):
    # Function to draw a hand from the center to the edge
    def draw_hand(angle, length, color):
        for i in range(1, length + 1):
            x = int(cos(radians(angle)) * i) + 3
            y = int(sin(radians(angle)) * i) + 3
            sense.set_pixel(max(0, min(7, x)), max(0, min(7, y)), color)

    sense.clear()
    now = datetime.now()
    seconds, minutes, hours = now.second, now.minute, now.hour

    draw_hand((seconds % 60) * 6, 5, [0, 255, 0])
    draw_hand((minutes % 60), 4, [255, 0, 0])
    draw_hand(((hours % 12) + minutes / 60) * 30, 3, [0, 0, 255])


# Joystick event handling
def joystick_moved(event, current_mode, total_modes):
    if event.action != "pressed":
        return current_mode

    if event.direction == "right":
        return (current_mode % total_modes) + 1

    if event.direction == "left":
        return (current_mode - 2) % total_modes + 1


def main():
    sense, mode = SenseHat(), 1

    try:
        while True:
            match mode:
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
                mode = joystick_moved(event, mode, 6)

            sleep(0.1)

    except KeyboardInterrupt:
        sense.clear()


if __name__ == "__main__":
    main()
