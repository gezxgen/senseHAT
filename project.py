from datetime import datetime
from sense_hat import SenseHat
from time import sleep


# Define mode functions
def binary_clock(sense):
    sense.clear()

    now = datetime.now()

    # Convert time to binary
    binary_hours = bin(now.hour)[2:].zfill(8)
    binary_minutes = bin(now.minute)[2:].zfill(8)
    binary_seconds = bin(now.second)[2:].zfill(8)

    # Initialize LED matrix with all off
    pixels = [[0, 0, 0] for _ in range(64)]

    # Define binary representation on the grid
    for i in range(8):
        # Hours (columns 0-1)
        if binary_hours[7 - i] == '1':
            pixels[i * 8] = [0, 0, 255]  # Blue for hours
            pixels[i * 8 + 1] = [0, 0, 255]

        # Minutes (columns 3-4)
        if binary_minutes[7 - i] == '1':
            pixels[i * 8 + 3] = [255, 0, 0]  # Red for minutes
            pixels[i * 8 + 4] = [255, 0, 0]

        # Seconds (columns 6-7)
        if binary_seconds[7 - i] == '1':
            pixels[i * 8 + 6] = [0, 255, 0]  # Green for seconds
            pixels[i * 8 + 7] = [0, 255, 0]

    # Update the LED matrix
    sense.set_pixels(pixels)


def binary_date(sense):
    sense.show_letter("2")


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
