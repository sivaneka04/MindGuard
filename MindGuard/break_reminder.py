import tkinter as tk
from tkinter import messagebox
import threading
import tkinter as tk
from tkinter import messagebox
import threading
import time
import winsound

from sidebar import Sidebar, APP_BG, CARD_BG, TEXT_COLOR, SUB_TEXT, GREEN, RED


class BreakPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=APP_BG)

        self.controller = controller

        Sidebar(self, controller).pack(side="left", fill="y")

        self.timer_running = False
        self.remaining_seconds = 0

        content = tk.Frame(self, bg=APP_BG)
        content.pack(side="left", fill="both", expand=True, padx=35, pady=25)

        tk.Label(
            content,
            text="Break Reminder",
            font=("Segoe UI", 28, "bold"),
            bg=APP_BG,
            fg="white"
        ).pack(pady=(5, 8))

        tk.Label(
            content,
            text="Set a break reminder to rest your eyes and reduce digital strain.",
            font=("Segoe UI", 12),
            bg=APP_BG,
            fg=SUB_TEXT
        ).pack(pady=(0, 30))

        card = tk.Frame(
            content,
            bg=CARD_BG,
            highlightbackground="#DDE6F3",
            highlightthickness=1
        )
        card.pack(padx=55, pady=5, fill="x")

        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(padx=40, pady=38, fill="both")

        tk.Label(
            inner,
            text="Set Reminder Time",
            font=("Segoe UI", 20, "bold"),
            bg=CARD_BG,
            fg=TEXT_COLOR
        ).pack(pady=(0, 18))

        tk.Label(
            inner,
            text="Enter the time interval before the next break reminder.",
            font=("Segoe UI", 11),
            bg=CARD_BG,
            fg="#667085"
        ).pack(pady=(0, 30))

        input_frame = tk.Frame(inner, bg=CARD_BG)
        input_frame.pack(pady=(0, 25))

        tk.Label(
            input_frame,
            text="Hours",
            font=("Segoe UI", 11, "bold"),
            bg=CARD_BG,
            fg=TEXT_COLOR
        ).grid(row=0, column=0, padx=18, pady=(0, 6))

        self.hour_entry = tk.Entry(
            input_frame,
            width=10,
            font=("Segoe UI", 13),
            justify="center"
        )
        self.hour_entry.grid(row=1, column=0, padx=18)
        self.hour_entry.insert(0, "0")

        tk.Label(
            input_frame,
            text="Minutes",
            font=("Segoe UI", 11, "bold"),
            bg=CARD_BG,
            fg=TEXT_COLOR
        ).grid(row=0, column=1, padx=18, pady=(0, 6))

        self.minute_entry = tk.Entry(
            input_frame,
            width=10,
            font=("Segoe UI", 13),
            justify="center"
        )
        self.minute_entry.grid(row=1, column=1, padx=18)
        self.minute_entry.insert(0, "1")

        self.status_label = tk.Label(
            inner,
            text="Reminder Status: No reminder set",
            font=("Segoe UI", 13, "bold"),
            bg=CARD_BG,
            fg=TEXT_COLOR
        )
        self.status_label.pack(pady=(15, 10))

        self.countdown_label = tk.Label(
            inner,
            text="Time Remaining: -",
            font=("Segoe UI", 12),
            bg=CARD_BG,
            fg="#667085"
        )
        self.countdown_label.pack(pady=(0, 25))

        button_frame = tk.Frame(inner, bg=CARD_BG)
        button_frame.pack(pady=(0, 25))

        self.set_button = tk.Button(
            button_frame,
            text="Set Reminder",
            font=("Segoe UI", 12, "bold"),
            bg=GREEN,
            fg="white",
            activebackground="#128C3A",
            activeforeground="white",
            width=16,
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.set_reminder
        )
        self.set_button.grid(row=0, column=0, padx=12)

        self.off_button = tk.Button(
            button_frame,
            text="Turn Off",
            font=("Segoe UI", 12, "bold"),
            bg=RED,
            fg="white",
            activebackground="#A82020",
            activeforeground="white",
            width=16,
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.turn_off_reminder
        )
        self.off_button.grid(row=0, column=1, padx=12)

        tk.Label(
            inner,
            text="Tip: regular short breaks can help reduce eye strain and improve focus.",
            font=("Segoe UI", 10),
            bg=CARD_BG,
            fg="#667085"
        ).pack(pady=(0, 0))

    def set_reminder(self):
        try:
            hours_text = self.hour_entry.get().strip()
            minutes_text = self.minute_entry.get().strip()

            if hours_text == "":
                hours_text = "0"

            if minutes_text == "":
                minutes_text = "0"

            hours = int(hours_text)
            minutes = int(minutes_text)

            if hours < 0 or minutes < 0:
                messagebox.showerror("Invalid Time", "Please enter positive numbers only.")
                return

            total_seconds = (hours * 3600) + (minutes * 60)

            if total_seconds <= 0:
                messagebox.showerror("Invalid Time", "Please enter at least 1 minute.")
                return

            # stop old timer first
            self.timer_running = False
            self.remaining_seconds = total_seconds

            # update app/report value
            self.controller.break_reminder_status = f"Reminder set: {hours}h {minutes}m"

            # update screen
            self.timer_running = True
            self.status_label.config(
                text=f"Reminder Status: Active ({hours}h {minutes}m)",
                fg=GREEN
            )
            self.update_countdown_label()

            # start countdown in background
            timer_thread = threading.Thread(target=self.run_timer, daemon=True)
            timer_thread.start()

            messagebox.showinfo(
                "Reminder Set",
                f"Break reminder set for {hours} hour(s) and {minutes} minute(s)."
            )

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter numbers only.")

    def run_timer(self):
        while self.timer_running and self.remaining_seconds > 0:
            time.sleep(1)
            self.remaining_seconds -= 1
            self.after(0, self.update_countdown_label)

        if self.timer_running and self.remaining_seconds <= 0:
            self.timer_running = False
            self.controller.break_reminder_status = "Reminder completed"
            self.after(0, self.show_break_alert)

    def update_countdown_label(self):
        if self.timer_running:
            total = self.remaining_seconds
            hours = total // 3600
            minutes = (total % 3600) // 60
            seconds = total % 60

            self.countdown_label.config(
                text=f"Time Remaining: {hours:02d}:{minutes:02d}:{seconds:02d}"
            )
        else:
            self.countdown_label.config(text="Time Remaining: -")

    def show_break_alert(self):
        self.status_label.config(
            text="Reminder Status: Break time reached",
            fg=RED
        )

        self.countdown_label.config(text="Time Remaining: 00:00:00")

        try:
            winsound.Beep(1000, 600)
            winsound.Beep(1200, 600)
        except:
            pass

        messagebox.showinfo(
            "Break Reminder",
            "It is time to take a short break.\n\nRest your eyes, stretch your body, and drink some water."
        )

    def turn_off_reminder(self):
        self.timer_running = False
        self.remaining_seconds = 0

        self.controller.break_reminder_status = "No reminder set"

        self.status_label.config(
            text="Reminder Status: No reminder set",
            fg=TEXT_COLOR
        )

        self.countdown_label.config(text="Time Remaining: -")

        messagebox.showinfo(
            "Reminder Off",
            "Break reminder has been turned off."
        )