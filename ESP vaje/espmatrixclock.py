import neopixel
from machine import ADC, Pin
from time import sleep
import time

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
        if digit > 1:
            start += 4
        self.setPixelColor((lineCoords[0][0] + start, lineCoords[0][1]), color)
        self.setPixelColor((lineCoords[1][0] + start, lineCoords[1][1]), color)

    def drawDigit(self, digit, value, color):
        valueSequence = Matrix.NUMBERS[value]
        for num in valueSequence:
            self.setLineColor(digit, num, color)

    def drawNumber(self, value, color, write=False):
        if self.currentNumber == value:
            return
        self.currentNumber = value
        if len(str(value)) < 4:
            value = f"{self.currentNumber:04d}"
        for i in range(len(str(value))):
            val = int(str(value)[i])
            self.drawDigit(i+max((4 - len(str(value))), 0), val, color)

        if write: self.neo.write()

    def cleanDisplay(self):
        self.drawNumber(8888, "BLANK", write=True)
    
    def flashNumber(self, num, color, delay, reps):
        for i in range(reps):
            self.cleanDisplay()
            sleep(delay)
            self.drawNumber(num, "WHITE", write=True)

    def drawDivider(self, color, write=True):
        matrix.drawNumber(0, color, write=True)
        matrix.setPixelColor((11, 2), color)
        matrix.setPixelColor((11, 4), color)
        matrix.neo.write()


def convertTime(minutes):
    return minutes // 60, minutes % 60
    
        
def potToSSdisplay(pot, matrix, refreshRate=0.5, endCondition=(None, False)):
    preTime = 0

    while True:
        if time.ticks_ms() > preTime + (refreshRate * 1000):
            matrix.cleanDisplay()

            potValue = pot.read()
            #potValue = TREBA DODELAT
            matrix.drawNumber(potValue, "WHITE", write=True)
            preTime = time.ticks_ms()
        
        if endCondition[0]:
            if (not endCondition[1] and endCondition[0]()) or (endCondition[1] and not endCondition[0]()):
                matrix.cleanDisplay()
                return potValue


def clockProtocol(matrix, pot, buttons, speed=1):
    STATE = "DEFAULT"
    ALARM_TIME = None
    DEF_previous = -60000
    CURRENT_TIME = 1430

    matrix.drawDivider("WHITE")
    while True:
        if STATE == "DEFAULT":
            if time.ticks_ms() > DEF_previous + (60000/speed):
                DEF_previous = time.ticks_ms()
                CURRENT_TIME += 1
                if CURRENT_TIME == 1440:
                    CURRENT_TIME = 0
                displayTime = convertTime(CURRENT_TIME)
                displayTime = int(f"{displayTime[0]:02d}{displayTime[1]:02d}")
                matrix.cleanDisplay()
                matrix.drawNumber(displayTime, "WHITE", write=True)

        elif STATE == "SET_ALARM":
            ALARM_TIME = potToSSdisplay(pot, matrix, endCondition=(buttons["OK"].value, True))
            matrix.flashNumber(ALARM_TIME, "WHITE", 0.2, 5)
            STATE = "DEFAULT"

        # Input queue
        if not buttons["OK"].value() and STATE == "DEFAULT":
            STATE = "SET_ALARM"




if __name__ == "__main__":
    matrix = Matrix(27, 23, 7)
    pot = ADC(Pin(34))
    buttons = {
        "OK": Pin(33, Pin.IN, Pin.PULL_UP)
    }
    clockProtocol(matrix, pot, buttons, speed=100)
    
