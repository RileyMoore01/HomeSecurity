import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Set up ultrasonic sensor pins
TRIG = 23
ECHO = 24

# Set up alarm pin
ALARM = 18
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(ALARM, GPIO.OUT)

def get_distance():
    # Trigger pulse
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    # Wait for echo
    while GPIO.input(ECHO) == GPIO.LOW:
        pulse_start = time.time()

    while GPIO.input(ECHO) == GPIO.HIGH:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound 34300 cm/s / 2

    return round(distance, 2)

def trigger_alarm():
    GPIO.output(ALARM, GPIO.HIGH)
    time.sleep(1)  # Alarm duration
    GPIO.output(ALARM, GPIO.LOW)

def monitor_distance(threshold):
    try:
        while True:
            distance = get_distance()
            print(f"Distance: {distance} cm")
            if distance < threshold:
                print("Intruder detected! Triggering alarm...")
                trigger_alarm()
            time.sleep(0.5)  # Delay between measurements
    except KeyboardInterrupt:
        print("Monitoring stopped.")
        cleanup()

# Clean up GPIO when done
def cleanup():
    GPIO.cleanup()

# Example usage
if __name__ == "__main__":
    DISTANCE_THRESHOLD = 50  # Set your threshold in cm
    monitor_distance(DISTANCE_THRESHOLD)