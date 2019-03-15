#!/usr/bin/env python3
from time import sleep, time
from flask import Flask
from board import SCL, SDA
from gpiozero import LED
from adafruit_seesaw.seesaw import Seesaw
import busio
import requests

ts = round(time())

power = LED(14)
power.on();
sleep(1);

i2c_bus = busio.I2C(SCL, SDA)
ss = Seesaw(i2c_bus, addr=0x36)

moistures = []

for x in range(10):
  moistures.append(ss.moisture_read())
  sleep(1)

moistures.sort()
del moistures[0]
del moistures[0]
moistures.pop()
moistures.pop()

sum = 0;

for x in moistures:
  sum += x

moisture = round(sum / len(moistures));
temp = ss.get_temp();

power.off();

payload = {'instanceId': 'testthree', 'timestamp': ts, 'level': moisture, 'temp': round(temp, 2)}
requests.get('https://us-central1-happyplantcloudfunctions.cloudfunctions.net/addMoistureUpdate', params=payload)