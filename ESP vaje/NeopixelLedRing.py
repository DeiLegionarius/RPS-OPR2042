from machine import Pin
import neopixel
from time import sleep
import random as rnd

pin = Pin(27, Pin.OUT)
np = neopixel.NeoPixel(pin, 50)

COLOR = {
    "BLANK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255)
}

def divide_pixels(neo, sections):
    pixels = len(neo)
    if pixels % sections == 0:
        divide = pixels / sections
        return int(divide)
    else:
        return False

def flush(neo, color, write=False):
    for i in range(len(neo)):
        neo[i] = color
    if write: np.write()

def colors_flash():
    global np
    current = False
    while True:
        current = not current
        for i in range(len(np)):
            if current:
                np[i] = 255, 0, 0
            else:
                np[i] = 0, 0, 255
            current = not current
        np.write()
        sleep(1)



def turn_periodically(divide):
    global np

    if not divide:
        while True:
            flush(np, (255, 0, 0), write=True)
            sleep(0.3)
            flush(np, (0, 0, 0), write=True)
            sleep(0.3)
    
    color = 0, 255, 0
    i = 0
    while True:
        flush(np, (0, 0, 0))
        for i2 in range(divide):
            np[i + i2] = color
        np.write()
        print("written")
        i += divide
        if i >= len(np):
            i -= len(np)
        sleep(1)
        

def flash(np, val, color1, color2, delay):
    np[val] = color1
    np.write()
    sleep(delay)
    np[val] = color2
    np.write()
    sleep(delay)

def ruletaBoard():
    global np

    flush(np, COLOR["BLANK"], write=True)
    for i in range(len(np)):
        if i == 0:
            np[i] = COLOR["GREEN"]
        elif i % 2 == 0:
            np[i] = COLOR["RED"]
        else:
            np[i] = COLOR["BLANK"]
    np.write()

def ruleta(div, speed, friction):
    global np

    #speed *= len(np)
    #friction *= len(np)

    ruletaBoard()

    ballpos = 0

    while speed > 0:

        if ballpos == 0:
            np[ballpos] = COLOR["GREEN"]
        elif ballpos % 2 == 0:
            np[ballpos] = COLOR["RED"]
        else:
            np[ballpos] = COLOR["BLANK"]

        ballpos = (ballpos + 1) % len(np)
        np[ballpos] = COLOR["WHITE"]
        np.write()
        sleep_time = max(min(0.1 / (speed * 0.1), 1), 0.01)
        print(f"speed={speed:.2f}, friction={friction:.4f}, sleep={sleep_time:.4f}")
        sleep(sleep_time)
        speed -= friction
        friction += 0.01 / speed

    if ballpos == 0:
        C2 = COLOR["GREEN"]
    elif ballpos % 2 == 0:
        C2 = COLOR["RED"]
    else:
        C2 = COLOR["BLANK"]

    while True:
        flash(np, ballpos, COLOR["WHITE"], C2, 0.2)

if __name__ == "__main__":
    # colors_flash()
    divide = divide_pixels(np, 8)
    # print(divide)
    # turn_periodically(divide)
    ruleta(divide, rnd.randint(50, 120), (rnd.randint(1, 2000) * 0.001))