from sense_hat import SenseHat
from time import sleep


# Define mode functions
def mode_1(sense):
    sense.show_message("1", scroll_speed=0)


def mode_2(sense):
    sense.show_message("2", scroll_speed=0)


def mode_3(sense):
    sense.show_message("3", scroll_speed=0)


def mode_4(sense):
    sense.show_message("4", scroll_speed=0)


def mode_5(sense):
    sense.show_message("5", scroll_speed=0)


def mode_6(sense):
    sense.show_message("6", scroll_speed=0)


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
                    mode_1(sense)
                case 2:
                    mode_2(sense)
                case 3:
                    mode_3(sense)
                case 4:
                    mode_4(sense)
                case 5:
                    mode_5(sense)
                case 6:
                    mode_6(sense)

            # Check for joystick events
            for event in sense.stick.get_events():
                current_mode = joystick_moved(event, current_mode, total_modes)

            sleep(0.1)
    except KeyboardInterrupt:
        sense.clear()


if __name__ == "__main__":
    main()
