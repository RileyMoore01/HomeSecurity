import tkinter as tk
from tkinter import ttk
import threading
import RPi.GPIO as GPIO
import time

# Pin Definitions
sound_pin = 17
alarm_pin = 27

# System Settings
ALARM_DURATION = 3
COOLDOWN_PERIOD = 5

# Flag to control monitoring thread
monitoring = False

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sound_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(alarm_pin, GPIO.OUT)
    GPIO.output(alarm_pin, GPIO.LOW)

def cleanup_gpio():
    GPIO.cleanup()

def monitor_sound(status_label):
    global monitoring
    while monitoring:
        if GPIO.input(sound_pin) == GPIO.LOW:
            status_label.config(text="🐶 Bark detected! Triggering alarm...", foreground="red")
            GPIO.output(alarm_pin, GPIO.HIGH)
            time.sleep(ALARM_DURATION)
            GPIO.output(alarm_pin, GPIO.LOW)
            status_label.config(text="⏳ Cooldown active...", foreground="orange")
            time.sleep(COOLDOWN_PERIOD)
        else:
            status_label.config(text="✅ Listening for barks...", foreground="green")
        time.sleep(0.1)

def start_monitoring(status_label):
    global monitoring
    if not monitoring:
        monitoring = True
        setup_gpio()
        status_label.config(text="✅ Listening for barks...", foreground="green")
        threading.Thread(target=monitor_sound, args=(status_label,), daemon=True).start()

def stop_monitoring(status_label):
    global monitoring
    if monitoring:
        monitoring = False
        GPIO.output(alarm_pin, GPIO.LOW)
        cleanup_gpio()
        status_label.config(text="⏹️ Monitoring stopped.", foreground="black")

# --- GUI Setup ---
def create_gui():
    root = tk.Tk()
    root.title("Dog Bark Alarm Control")
    root.geometry("400x200")
    root.resizable(False, False)

    # Title Label
    ttk.Label(root, text="🐾 Dog Bark Detection System", font=("Helvetica", 16)).pack(pady=10)

    # Status Label
    status_label = ttk.Label(root, text="System is idle.", font=("Helvetica", 12))
    status_label.pack(pady=10)

    # Button Frame
    btn_frame = ttk.Frame(root)
    btn_frame.pack(pady=10)

    # Start Button
    start_btn = ttk.Button(btn_frame, text="Start Monitoring", command=lambda: start_monitoring(status_label))
    start_btn.grid(row=0, column=0, padx=10)

    # Stop Button
    stop_btn = ttk.Button(btn_frame, text="Stop Monitoring", command=lambda: stop_monitoring(status_label))
    stop_btn.grid(row=0, column=1, padx=10)

    # Exit Button
    exit_btn = ttk.Button(root, text="Exit", command=lambda: on_exit(root))
    exit_btn.pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", lambda: on_exit(root))
    root.mainloop()

def on_exit(root):
    stop_monitoring(status_label=None)  # Safe even if not monitoring
    root.destroy()

if __name__ == "__main__":
    create_gui()
