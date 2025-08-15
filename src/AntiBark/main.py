import tkinter as tk
from tkinter import ttk
import threading
import RPi.GPIO as GPIO
import time

# GPIO Pins
SOUND_PIN = 17
ALARM_PIN = 27

# Settings
ALARM_DURATION = 3
COOLDOWN_PERIOD = 5

# Monitoring control
monitoring = False


# --- GPIO Setup ---
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SOUND_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ALARM_PIN, GPIO.OUT)
    GPIO.output(ALARM_PIN, GPIO.LOW)


def cleanup_gpio():
    GPIO.cleanup()


# --- Sound Monitor Thread ---
def monitor_sound(status_label, sound_label):
    global monitoring
    while monitoring:
        sound_state = GPIO.input(SOUND_PIN)
        if sound_state == GPIO.LOW:
            status_label.config(text="Bark detected!", foreground="#ff4d4d")
            sound_label.config(text="Sound: LOW (Detected)", foreground="#ff4d4d")
            GPIO.output(ALARM_PIN, GPIO.HIGH)
            time.sleep(ALARM_DURATION)
            GPIO.output(ALARM_PIN, GPIO.LOW)
            status_label.config(text="Cooldown...", foreground="#ffaa00")
            time.sleep(COOLDOWN_PERIOD)
        else:
            status_label.config(text="✅ Listening...", foreground="#33cc33")
            sound_label.config(text="Sound: HIGH (Quiet)", foreground="#33cc33")
        time.sleep(0.2)

def toggle_monitoring(toggle_btn, status_label, sound_label):
    global monitoring
    if not monitoring:
        monitoring = True
        toggle_btn.config(text="Stop Monitoring", style="Red.TButton")
        setup_gpio()
        threading.Thread(
            target=monitor_sound, args=(status_label, sound_label), daemon=True
        ).start()
    else:
        monitoring = False
        GPIO.output(ALARM_PIN, GPIO.LOW)
        cleanup_gpio()
        status_label.config(text="Monitoring stopped.", foreground="#666")
        sound_label.config(text="Sound: --", foreground="#666")
        toggle_btn.config(text="▶️ Start Monitoring", style="Green.TButton")


def stop_monitoring(status_label, sound_label):
    global monitoring
    if monitoring:
        monitoring = False
        GPIO.output(ALARM_PIN, GPIO.LOW)
        cleanup_gpio()
        status_label.config(text="Monitoring stopped.", foreground="#666")
        sound_label.config(text="Sound: --", foreground="#666")
        
        
# --- GUI ---
def create_gui():
    root = tk.Tk()
    root.title("Dog Bark Alarm")
    root.geometry("600x400")
    root.configure(bg="#f9f9f9")
    root.resizable(False, False)

    style = ttk.Style(root)
    style.theme_use("clam")

    # Base styles
    style.configure("TButton", font=("Segoe UI", 12), padding=10)
    style.configure("TLabel", background="#f9f9f9")

    # Toggle button styles
    style.configure("Green.TButton", background="#4CAF50", foreground="white")
    style.map("Green.TButton",
              background=[("active", "#45a049")])
    style.configure("Red.TButton", background="#f44336", foreground="white")
    style.map("Red.TButton",
              background=[("active", "#e53935")])

    # --- Title ---
    ttk.Label(
        root,
        text="Dog Bark Detection System",
        font=("Segoe UI", 20, "bold"),
        foreground="#333",
    ).pack(pady=20)

    # --- Status Display ---
    status_label = ttk.Label(
        root, text="System is idle.", font=("Segoe UI", 14), foreground="#666"
    )
    status_label.pack(pady=10)

    # --- Sound Level Display ---
    sound_label = ttk.Label(
        root, text="Sound: --", font=("Segoe UI", 12), foreground="#666"
    )
    sound_label.pack(pady=5)

    # --- Toggle Button ---
    toggle_btn = ttk.Button(
        root,
        text="Start Monitoring",
        style="Green.TButton",
        command=lambda: toggle_monitoring(toggle_btn, status_label, sound_label),
    )
    toggle_btn.pack(pady=30)

    # --- Exit ---
    ttk.Button(
        root,
        text="Exit",
        command=lambda: on_exit(root, status_label, sound_label),
    ).pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", lambda: on_exit(root, status_label, sound_label))
    root.mainloop()


def on_exit(root, status_label, sound_label):
    stop_monitoring(status_label, sound_label)
    root.destroy()


if __name__ == "__main__":
    create_gui()
