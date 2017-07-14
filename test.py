import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN)

while True:
  i = GPIO.input(16)
  if (i == 0):
    print("No one there")
  elif (i == 1):
    print("Motion Detected.")
  time.sleep(.5)
