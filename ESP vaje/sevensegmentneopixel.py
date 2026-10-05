import neopixel
from machine import ADC, Pin
from time import sleep

COLOR = {
    "BLANK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255)
}

NUMBERS = []

class Matrix:
    LINES = [((1, 0), (2, 0)), ((0, 1), (0, 2)), ((3, 1), (3, 2)), ((1, 3), (2, 3)), ((0, 4), (0, 5)), ((3, 4), (3, 5)), ((1, 6), (2, 6))]

    NUMBERS = [(0, 1, 2, 4, 5, 6), (2, 5), (0, 2, 3, 4, 6), (0, 2, 3, 5, 6), (1, 3, 5, 2), (0, 1, 3, 5, 6), (0, 1, 3, 4, 5, 6), (0, 2, 5), (0, 1, 2, 3, 4, 5, 6), (0, 1, 2, 3, 5, 6)]

    def __init__(self, pin, length, height):
        self.length = length
        self.height = height
        self.pixels = length * height
        self.pinis = Pin(pin, Pin.OUT)
        self.neo = neopixel.NeoPixel(self.pinis, self.pixels)
        self.currentNumber = None

    def getPixelNumber(self, x, y):
        length = y * self.length
        pos = length + x
        return pos

    def setPixelColor(self, pos: tuple, color):
        pos = self.getPixelNumber(pos[0], pos[1])
        color = COLOR[color]
        self.neo[pos] = color

    def setLineColor(self, digit, lineNum, color):
        lineCoords = Matrix.LINES[lineNum]
        start = (digit * 5)
        self.setPixelColor((lineCoords[0][0] + start, lineCoords[0][1]), color)
        self.setPixelColor((lineCoords[1][0] + start, lineCoords[1][1]), color)

    def drawDigit(self, digit, value, color):
        valueSequence = Matrix.NUMBERS[value]
        for num in valueSequence:
            self.setLineColor(digit, num, color)

    def drawNumber(self, value, color, write=False):
        if self.currentNumber == value:
            return
        for i in range(len(str(value))):
            val = int(str(value)[i])
            self.drawDigit(i+max((4 - len(str(value))), 0), val, color)

        if write: self.neo.write()

    def cleanDisplay(self):
        self.drawNumber(8888, "BLANK", write=True)

        
        
def potToSSdisplay(pot, matrix):
    while True:
        potValue = pot.read()
        matrix.drawNumber(potValue, "WHITE", write=True)
        print(potValue)
        sleep(0.5)
        matrix.cleanDisplay()

    

if __name__ == "__main__":
    matrix = Matrix(27, 20, 7)
    pot = ADC(Pin(34))
    potToSSdisplay(pot, matrix)
