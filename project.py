from sense_hat import SenseHat
from time import sleep


# Define mode functions
def binary_clock(sense):
    sense.show_letter("1", scroll_speed=0)


def binary_date(sense):
    sense.show_letter("2", scroll_speed=0)


def analog_clock(sense):
    sense.show_letter("3", scroll_speed=0)


def water_scale(sense):
    sense.show_letter("4", scroll_speed=0)


def temperature(sense):
    sense.show_letter("5", scroll_speed=0)


def internet(sense):
    sense.show_letter("6", scroll_speed=0)


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
