# Built using the firmata library for arduino
# Built for python 3.10.11
# tested on Arduino UNO-R3
# install the modified version of firmata to the arduino before running this code ("StandardFirmata_lcdModification.ino")


import time
import pyfirmata as pyfirmata

# setup serial communication
PORT = "COM6"  # change to whatever port is in use by your arduino
board = pyfirmata.Arduino(PORT)


time.sleep(4)  # give time for the arduino to connect and start before running code

# not really sure why this is here but it breaks without it
it = pyfirmata.util.Iterator(board)
it.start()


# interfaces to make it easier to run the arduinos
class LCD:

    rarr = chr(0x7E)
    larr = chr(0x7F)

    def __init__(self) -> None:
        self.line1, self.line2 = "", ""

    def write(self, line1="", line2="") -> None:
        if type(line1) is not str or type(line2) is not str:
            raise TypeError("line1 and line2 must be strings in LCD.write()")
        if len(line1) > 16 or len(line2) > 16:
            raise ValueError(
                "line1 and line2 can be a maximum of 16 charachters in LCD.write()"
            )
        self.line1 = line1
        self.line2 = line2
        board.send_sysex(
            pyfirmata.STRING_DATA, pyfirmata.util.str_to_two_byte_iter(line1)
        )
        board.send_sysex(
            pyfirmata.STRING_DATA, pyfirmata.util.str_to_two_byte_iter(line2)
        )

    def clear(self) -> None:
        self.write()

    def get_text(self) -> list[str]:
        return [self.line1, self.line2]


class AnalogInput:
    def __init__(self, pin: int) -> None:
        self.pin = board.get_pin(f"a:{pin}:i")

    def as_digital(self) -> bool:
        return (
            (self.pin.read() >= 0.7)
            if self.pin.read() >= 0.7 or self.pin.read() <= 0.3
            else None
        )

    def as_volts(self) -> float:
        return self.pin.read() * 5

    def as_analogInt(self) -> int:
        return int(self.pin.read() * 1023)

    def as_analog(self) -> float:
        return self.pin.read()


class DigitalInput(AnalogInput):
    def __init__(self, pin: int) -> None:
        self.pin = board.get_pin(f"d:{pin}:i")

    def as_digital(self) -> bool:
        return self.pin.read()

    def as_analog(self) -> float:
        return int(self.pin.read())


class DigitalOutput:
    def __init__(self, pin: int, status=0) -> None:
        self.pin = board.get_pin(f"d:{pin}:o")
        self.pin.write(status)

    def on(self) -> None:
        self.pin.write(1)

    def off(self) -> None:
        self.pin.write(0)


class AnalogOutput:
    def __init__(self, pin: int, status=0) -> None:
        self.pin = board.get_pin(f"a:{pin}:o")
        self.pin.write(status)

    def on(self, value=1023) -> None:
        self.pin.write(value)

    def off(self) -> None:
        self.pin.write(0)


# sets up IO ports

lcd = LCD()


class button:
    up = AnalogInput(1)
    down = AnalogInput(2)
    left = AnalogInput(3)
    right = AnalogInput(0)
    a = AnalogInput(5)
    b = AnalogInput(4)
    dpad = [up, down, left, right]
    all = dpad + [a, b]


class LEDs:
    cyan = DigitalOutput(2)
    white = DigitalOutput(3)
    red = DigitalOutput(4)
    yellow = DigitalOutput(5)
    green = DigitalOutput(7)
    blue = DigitalOutput(6)
    all = [cyan, white, red, yellow, green, blue]

    def all_on() -> None:
        [LED.on() for LED in LEDs.all]

    def all_off() -> None:
        [LED.off() for LED in LEDs.all]


##EXAMPLES

# write text to the lcd (two lines of width 16 charachters)
# only write to the LCD screen at least 150ms after previously writing as it may cause errors to occur that will not be caught by the code
lcd.write("text line 1", "text line 2")

# clear LCD screen
lcd.clear()

# get text currently on the LCD screen ass array [line1,line2]
lcd.get_text()

# turn on/off specific LED (colours are white, yellow, green, blue,red,cyan)
LEDs.blue.on()
LEDs.yellow.off()

# turn on/off ALL LEDs
LEDs.all_on()
LEDs.all_off()

# get input from specific button (a,b,up,down,left,right => returns True when pressed, and False if not. returns None if there is an error)
button.a.as_digital()
button.left.as_digital()

# get input from dpad as array of [up,down,left,right]
[b.as_digital() for b in button.dpad]
