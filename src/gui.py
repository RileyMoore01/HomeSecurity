import tkinter as tk
from tkinter import messagebox
import threading
import time
import sensor  # Import the sensor module we created

class SecuritySystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Home Security System")

        self.status_label = tk.Label(root, text="System Status: Disarmed", font=("Helvetica", 16))
        self.status_label.pack(pady=10)

        self.distance_label = tk.Label(root, text="Current Distance: --- cm", font=("Helvetica", 12))
        self.distance_label.pack(pady=5)

        self.arm_button = tk.Button(root, text="Arm System", command=self.arm_system, font=("Helvetica", 12))
        self.arm_button.pack(pady=5)

        self.disarm_button = tk.Button(root, text="Disarm System", command=self.disarm_system, font=("Helvetica", 12))
        self.disarm_button.pack(pady=5)

        self.alert_label = tk.Label(root, text="", font=("Helvetica", 12, 'bold'), fg="red")
        self.alert_label.pack(pady=5)

        self.running = False

    def arm_system(self):
        self.status_label.config(text="System Status: Armed")
        self.running = True
        self.check_distance()

    def disarm_system(self):
        self.status_label.config(text="System Status: Disarmed")
        self.running = False
        self.alert_label.config(text="")

    def check_distance(self):
        if self.running:
            distance = sensor.get_distance()  # Get distance from sensor
            self.distance_label.config(text=f"Current Distance: {distance} cm")

            if distance < 50:  # Trigger alert if something is too close
                self.alert_label.config(text="ALERT! Motion Detected!")
            else:
                self.alert_label.config(text="")

            # Repeat every second
            self.root.after(1000, self.check_distance)


def start_gui():
    root = tk.Tk()
    gui = SecuritySystemGUI(root)
    root.mainloop()

# Run the GUI in a separate thread so we can interact with the system
if __name__ == "__main__":
    gui_thread = threading.Thread(target=start_gui)
    gui_thread.daemon = True
    gui_thread.start()
