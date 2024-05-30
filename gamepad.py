import pyfirmata2 as pyfirmata

PORT = "COM6"
board = pyfirmata.Arduino(PORT)


write_lcd = lambda line1="", line2="": [
    board.send_sysex(pyfirmata.STRING_DATA, pyfirmata.util.str_to_two_byte_iter(data))
    for data in [line1, line2]
]


class buttons:
    up = board.get_pin("a:1:i")
    down = board.get_pin("a:2:i")
    left = board.get_pin("a:3:i")
    right = board.get_pin("a:0:i")
