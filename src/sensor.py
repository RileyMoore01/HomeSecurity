import tkinter as tk
from tkinter import messagebox
import threading
import time
import sensor  # Import the sensor module we created

class SecuritySystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Home Security System")
        
        # Initially, show password window
        self.show_password_window()

        self.status_label = None
        self.distance_label = None
        self.arm_button = None
        self.disarm_button = None
        self.alert_label = None
        self.running = False

    def show_password_window(self):
        """Shows password window when the app starts."""
        self.password_window = tk.Toplevel(self.root)
        self.password_window.title("Enter Password")
        
        self.password_label = tk.Label(self.password_window, text="Enter Password:", font=("Helvetica", 14))
        self.password_label.pack(pady=10)
        
        self.password_entry = tk.Entry(self.password_window, show="*", font=("Helvetica", 12))
        self.password_entry.pack(pady=10)

        self.password_button = tk.Button(self.password_window, text="Submit", command=self.check_password, font=("Helvetica", 12))
        self.password_button.pack(pady=10)

    def check_password(self):
        """Checks the entered password and grants access to the system."""
        entered_password = self.password_entry.get()

        # Hardcoded password (you can change it to something else)
        correct_password = "1234"

        if entered_password == correct_password:
            self.password_window.destroy()
            self.setup_gui()  # Set up the security system GUI after successful login
        else:
            messagebox.showerror("Incorrect Password", "The password you entered is incorrect.")
            self.password_entry.delete(0, tk.END)  # Clear the entry field

    def setup_gui(self):
        """Sets up the main security system GUI."""
        # Setup GUI components
        self.status_label = tk.Label(self.root, text="System Status: Disarmed", font=("Helvetica", 16))
        self.status_label.pack(pady=10)

        self.distance_label = tk.Label(self.root, text="Current Distance: --- cm", font=("Helvetica", 12))
        self.distance_label.pack(pady=5)

        self.arm_button = tk.Button(self.root, text="Arm System", command=self.arm_system, font=("Helvetica", 12))
        self.arm_button.pack(pady=5)

        self.disarm_button = tk.Button(self.root, text="Disarm System", command=self.disarm_system, font=("Helvetica", 12))
        self.disarm_button.pack(pady=5)

        self.alert_label = tk.Label(self.root, text="", font=("Helvetica", 12, 'bold'), fg="red")
        self.alert_label.pack(pady=5)

        self.running = False

    def arm_system(self):
        """Arms the system to start monitoring distance."""
        self.status_label.config(text="System Status: Armed")
        self.running = True
        self.check_distance()

    def disarm_system(self):
        """Disarms the system and stops monitoring."""
        self.status_label.config(text="System Status: Disarmed")
        self.running = False
        self.alert_label.config(text="")

    def check_distance(self):
        """Checks the distance from the ultrasonic sensor."""
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
