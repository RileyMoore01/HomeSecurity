import RPi.GPIO as GPIO
import time

# Pin Definitions
sound_pin = 17  # GPIO pin connected to the sound sensor's Digital Out (DO)
alarm_pin = 27  # GPIO pin connected to your alarm's signal input

# --- System Configuration ---
ALARM_DURATION = 3  # How long the alarm sounds in seconds
COOLDOWN_PERIOD = 5 # Time to wait after an alarm to avoid multiple triggers

def setup():
    """Sets up the GPIO pins."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sound_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Use pull-up resistor
    GPIO.setup(alarm_pin, GPIO.OUT)
    GPIO.output(alarm_pin, GPIO.LOW)  # Ensure alarm is off at the start
    print("System setup complete. Waiting for dog barks...")

def main():
    """Main loop to monitor sound and trigger alarm."""
    try:
        setup()
        while True:
            # The sound sensor's digital pin is LOW when a sound is detected
            if GPIO.input(sound_pin) == GPIO.LOW:
                print("Bark detected! Sounding alarm...")
                GPIO.output(alarm_pin, GPIO.HIGH) # Turn on the alarm
                time.sleep(ALARM_DURATION)        # Keep alarm on for a set duration
                GPIO.output(alarm_pin, GPIO.LOW)  # Turn off the alarm
                print("Alarm silenced. Waiting for cooldown...")
                time.sleep(COOLDOWN_PERIOD)       # Wait to prevent repeated alarms

            time.sleep(0.1) # Small delay to reduce CPU usage

    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    finally:
        GPIO.cleanup()  # Clean up all GPIO pins to release resources

if __name__ == '__main__':
    main()
