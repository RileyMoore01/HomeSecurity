import RPi.GPIO as GPIO
import time

SOUND_PIN = 17  # GPIO connected to DO pin

GPIO.setmode(GPIO.BCM)
GPIO.setup(SOUND_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Listening for sound... (Press Ctrl+C to exit)")

try:
    while True:
        if GPIO.input(SOUND_PIN) == GPIO.LOW:
            print("🔊 Sound detected!")
        else:
            print("🔇 Quiet")
        time.sleep(0.3)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
