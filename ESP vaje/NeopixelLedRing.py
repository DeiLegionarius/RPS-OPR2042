from machine import Pin
import neopixel
from time import sleep

pin = Pin(27, Pin.OUT)
np = neopixel.NeoPixel(pin, 16)

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
        
    



if __name__ == "__main__":
    # colors_flash()
    divide = divide_pixels(np, 8)
    print(divide)
    turn_periodically(divide)