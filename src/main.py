import sensor
import gui
import time

# Main program loop
if __name__ == "__main__":
    try:
        print("Starting Home Security System...")
        gui.start_gui()  # Start GUI on a separate thread

        # Keep the system running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Exiting system...")
        sensor.cleanup()  # Cleanup GPIO when done
