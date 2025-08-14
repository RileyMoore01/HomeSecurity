import RPi.GPIO as GPIO
import time

# GPIO pin connected to alarm
ALARM_PIN = 27
TEST_DURATION = 3  # Seconds

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ALARM_PIN, GPIO.OUT)
    GPIO.output(ALARM_PIN, GPIO.LOW)

def cleanup():
    GPIO.output(ALARM_PIN, GPIO.LOW)
    GPIO.cleanup()

def test_alarm():
    print(f"\nActivating alarm for {TEST_DURATION} seconds...")
    GPIO.output(ALARM_PIN, GPIO.HIGH)
    time.sleep(TEST_DURATION)
    GPIO.output(ALARM_PIN, GPIO.LOW)
    print("Alarm test completed.\n")

def main():
    setup()
    try:
        while True:
            choice = input("Press [Enter] to test alarm or type 'q' to quit: ").strip().lower()
            if choice == "q":
                break
            test_alarm()
    except KeyboardInterrupt:
        print("\nTest interrupted.")
    finally:
        cleanup()
        print("GPIO cleaned up. Exiting.")

if __name__ == "__main__":
    main()
