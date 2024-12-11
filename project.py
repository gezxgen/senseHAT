from datetime import datetime
from sense_hat import SenseHat
from time import sleep


def binary_clock(sense):
    sense.clear()

    now = datetime.now()

    # Convert time to binary
    binary_hours = bin(now.hour)[2:].zfill(8)
    binary_minutes = bin(now.minute)[2:].zfill(8)
    binary_seconds = bin(now.second)[2:].zfill(8)

    # Initialize LED matrix with all off
    pixels = [[0, 0, 0] for _ in range(64)]

    # Define binary representation on the grid, shifting down 2 pixels
    for i in range(8):
        # Hours (columns 0-1)
        if binary_hours[7 - i] == '1':
            pixels[(i + 2) * 8] = [0, 0, 255]  # Blue for hours (shifted down)
            pixels[(i + 2) * 8 + 1] = [0, 0, 255]

        # Minutes (columns 3-4)
        if binary_minutes[7 - i] == '1':
            pixels[(i + 2) * 8 + 3] = [255, 0, 0]  # Red for minutes (shifted down)
            pixels[(i + 2) * 8 + 4] = [255, 0, 0]

        # Seconds (columns 6-7)
        if binary_seconds[7 - i] == '1':
            pixels[(i + 2) * 8 + 6] = [0, 255, 0]  # Green for seconds (shifted down)
            pixels[(i + 2) * 8 + 7] = [0, 255, 0]

    # Update the LED matrix
    sense.set_pixels(pixels)


def binary_date(sense):
    sense.clear()

    # Get current date and time
    now = datetime.now()

    # Create a list of pixels to display and variables
    pixels = [[0, 0, 0] for _ in range(64)]
    year_binary = bin(now.year)[2:].zfill(16)
    month_binary = bin(now.month)[2:].zfill(8)
    day_binary = bin(now.day)[2:].zfill(8)
    weekday_binary = bin(now.weekday() + 1)[2:].zfill(8)

    for i in range(8):
        # Year (first 2 columns) - Purple
        if year_binary[15 - i] == '1':
            pixels[i * 8] = [128, 0, 128]  # Purple
            pixels[i * 8 + 1] = [128, 0, 128]

        # Month (next 2 columns) - Cyan
        if month_binary[7 - i] == '1':
            pixels[i * 8 + 2] = [0, 255, 255]  # Cyan
            pixels[i * 8 + 3] = [0, 255, 255]

        # Day (next 2 columns) - Yellow
        if day_binary[7 - i] == '1':
            pixels[i * 8 + 4] = [255, 255, 0]  # Yellow
            pixels[i * 8 + 5] = [255, 255, 0]

        # Weekday (next 2 columns) - Orange
        if weekday_binary[7 - i] == '1':
            pixels[i * 8 + 6] = [255, 165, 0]  # Orange
            pixels[i * 8 + 7] = [255, 165, 0]

    # Update the LED matrix
    sense.set_pixels(pixels)


def analog_clock(sense):
    sense.show_letter("3")


def water_scale(sense):
    sense.show_letter("4")


def temperature(sense):
    sense.show_letter("5")


def internet(sense):
    sense.show_letter("6")


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
