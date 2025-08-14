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
            status_label.config(text="🐶 Bark detected!", foreground="#ff4d4d")
            sound_label.config(text="Sound: LOW (Detected)", foreground="#ff4d4d")
            GPIO.output(ALARM_PIN, GPIO.HIGH)
            time.sleep(ALARM_DURATION)
            GPIO.output(ALARM_PIN, GPIO.LOW)
            status_label.config(text="⏳ Cooldown...", foreground="#ffaa00")
            time.sleep(COOLDOWN_PERIOD)
        else:
            status_label.config(text="✅ Listening...", foreground="#33cc33")
            sound_label.config(text="Sound: HIGH (Quiet)", foreground="#33cc33")
        time.sleep(0.2)


def start_monitoring(status_label, sound_label):
    global monitoring
    if not monitoring:
        monitoring = True
        setup_gpio()
        threading.Thread(
            target=monitor_sound, args=(status_label, sound_label), daemon=True
        ).start()


def stop_monitoring(status_label, sound_label):
    global monitoring
    if monitoring:
        monitoring = False
        GPIO.output(ALARM_PIN, GPIO.LOW)
        cleanup_gpio()
        status_label.config(text="⏹️ Monitoring stopped.", foreground="#666")
        sound_label.config(text="Sound: --", foreground="#666")


# --- GUI ---
def create_gui():
    root = tk.Tk()
    root.title("🐾 Dog Bark Alarm")
    root.geometry("450x300")
    root.configure(bg="#f2f2f2")
    root.resizable(False, False)

    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure("TButton", font=("Segoe UI", 11), padding=10)
    style.configure("TLabel", background="#f2f2f2")

    # --- Title ---
    ttk.Label(
        root,
        text="Dog Bark Detection System",
        font=("Segoe UI", 18, "bold"),
        foreground="#333",
    ).pack(pady=15)

    # --- Status Display ---
    status_label = ttk.Label(
        root, text="System is idle.", font=("Segoe UI", 14), foreground="#666"
    )
    status_label.pack(pady=5)

    # --- Sound Level Display ---
    sound_label = ttk.Label(
        root, text="Sound: --", font=("Segoe UI", 12), foreground="#666"
    )
    sound_label.pack(pady=5)

    # --- Buttons ---
    btn_frame = ttk.Frame(root)
    btn_frame.pack(pady=20)

    start_btn = ttk.Button(
        btn_frame,
        text="▶ Start Monitoring",
        command=lambda: start_monitoring(status_label, sound_label),
    )
    start_btn.grid(row=0, column=0, padx=10)

    stop_btn = ttk.Button(
        btn_frame,
        text="⏹ Stop Monitoring",
        command=lambda: stop_monitoring(status_label, sound_label),
    )
    stop_btn.grid(row=0, column=1, padx=10)

    # --- Exit ---
    exit_btn = ttk.Button(
        root, text="Exit", command=lambda: on_exit(root, status_label, sound_label)
    )
    exit_btn.pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", lambda: on_exit(root, status_label, sound_label))
    root.mainloop()


def on_exit(root, status_label, sound_label):
    stop_monitoring(status_label, sound_label)
    root.destroy()


if __name__ == "__main__":
    create_gui()
