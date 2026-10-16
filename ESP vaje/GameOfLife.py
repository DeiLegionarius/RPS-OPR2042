import neopixel
from machine import ADC, Pin
from time import sleep
import time

COLS = 8 #x
ROWS = 8 #y

NEO_PIN = 32

neo = neopixel.NeoPixel(NEO_PIN, COLS * ROWS)

def getPixelNumber(x, y):
        length = y * ROWS
        pos = length + x
        return pos

def setPixelColor(neo, pos: tuple, color):
    pos = getPixelNumber(pos[0], pos[1])
    color = COLOR[color]
    neo[pos] = color

def clean(neo, color=(0, 0, 0)):
    for x in range(ROWS):
        for y in range(COLS):
            neo[i] = color

def initCellMap():
    cellMap = []
    for x in range(ROWS):
        entry = []
        for y in range(COLS):
            entry.append(y)
        cellMap.append(entry)
    return cellMap

if __name__ == "__main__":
    
    
