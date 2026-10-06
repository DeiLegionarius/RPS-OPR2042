from machine import Pin, ADC, PWM
import neopixel
from time import sleep
import time

# Naprave
gumb = Pin(19, Pin.IN, Pin.PULL_UP)
pot = ADC(Pin(27))
neo_manjsi = neopixel.NeoPixel(Pin(14), 3)
neo_vecji = neopixel.NeoPixel(Pin(26), 10)
servo = PWM(Pin(32), freq=50)

# Konfiguracija
REFRESH_RATE = 500

GESLO = (6, 6, 6)
VPISANO_GESLO = []
TRENUTNA_ST = 0

LAST_REF_TIME = 0

LAST_PRESS_TIME = 0
BUTTON_COOLDOWN = 1000

POSKUSI = 3


def potOfNum(pot, num):
    val = pot.read() / 4095
    return val * num

def cleanNeo(neo, barva=[0, 0, 0], write=False):
    for i in range(len(neo)):
        neo[i] = barva
    if write: neo.write()

def flash(neo, rep, color, delay):
    for i in range(rep):
        cleanNeo(neo, barva=color, write=True)
        sleep(delay)
        cleanNeo(neo, barva=[0, 0, 0], write=True)
        sleep(delay)

def set_angle(servo, angle):
    min_us = 500
    max_us = 2500
    pulse_us = min_us + (max_us - min_us) * angle / 180
    duty = int(pulse_us * 65535 / 20000)
    print("servus")
    servo.duty_u16(duty)

cleanNeo(neo_manjsi, write=True)
while True:
    if TRENUTNA_ST != 3:
        if time.ticks_ms() > LAST_REF_TIME + REFRESH_RATE:
            cleanNeo(neo_vecji)
            trenuta_num = int(potOfNum(pot, 10))
            for i in range(trenuta_num):
                neo_vecji[i] = [255, 255, 255]
            neo_vecji.write()
            LAST_REF_TIME = time.ticks_ms()

        
        # Event queue
        if not gumb.value() and time.ticks_ms() > LAST_PRESS_TIME + BUTTON_COOLDOWN:
            VPISANO_GESLO.append(trenuta_num)
            TRENUTNA_ST += 1
            neo_manjsi[TRENUTNA_ST-1] = [255, 255, 255]
            neo_manjsi.write()
            LAST_PRESS_TIME = time.ticks_ms()
    
    else:
        if tuple(VPISANO_GESLO) == GESLO: # Geslo je pravilno
            cleanNeo(neo_manjsi, barva=[0, 255, 0], write=True)
            set_angle(servo, 90)
            break
        else: # Geslo je napačno
            cleanNeo(neo_manjsi, barva=[255, 0, 0], write=True)
            POSKUSI -= 1
            if POSKUSI == 0:
                flash(neo_manjsi, 3, [255, 0, 0], 0.5)

        sleep(0.5)
        TRENUTNA_ST = 0
        cleanNeo(neo_manjsi, write=True)
