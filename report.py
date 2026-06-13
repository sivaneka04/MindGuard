import tkinter as tk
import time

from sidebar import Sidebar, APP_BG, CARD_BG, TEXT_COLOR, SUB_TEXT, ACCENT, GREEN


class ReportPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=APP_BG)

        self.controller = controller

        Sidebar(self, controller).pack(side="left", fill="y")

        # Main content
        content = tk.Frame(self, bg=APP_BG)
        content.pack(side="left", fill="both", expand=True, padx=35, pady=25)

        # Page title
        tk.Label(
            content,
            text="Report and Summary",
            font=("Segoe UI", 28, "bold"),
            bg=APP_BG,
            fg="white"
        ).pack(anchor="w", pady=(0, 5))

        tk.Label(
            content,
            text="Generate a simple wellness summary based on screen time, stress level and reminder activity.",
            font=("Segoe UI", 12),
            bg=APP_BG,
            fg=SUB_TEXT
        ).pack(anchor="w", pady=(0, 25))

        # Outer white card
        card = tk.Frame(
            content,
            bg=CARD_BG,
            highlightbackground="#DDE6F3",
            highlightthickness=1
        )
        card.pack(pady=5, padx=60, fill="x")

        # Inner card
        inner = tk.Frame(card, bg=CARD_BG)
        inner.pack(padx=45, pady=30, fill="both")

        tk.Label(
            inner,
            text="MindGuard Overall Report",
            font=("Segoe UI", 22, "bold"),
            bg=CARD_BG,
            fg=ACCENT
        ).pack(pady=(0, 20))

        # Report display box
        report_box = tk.Frame(
            inner,
            bg="#F4F7FB",
            width=760,
            height=230
        )
        report_box.pack(pady=(0, 22))
        report_box.pack_propagate(False)

        self.report_text = tk.Label(
            report_box,
            text="Click Generate Report to view your wellness summary.",
            font=("Segoe UI", 13),
            bg="#F4F7FB",
            fg=TEXT_COLOR,
            justify="left",
            anchor="nw",
            wraplength=700
        )
        self.report_text.pack(fill="both", expand=True, padx=30, pady=22)

        # Generate button
        tk.Button(
            inner,
            text="Generate Report",
            font=("Segoe UI", 12, "bold"),
            bg=GREEN,
            fg="white",
            activebackground="#128C3A",
            activeforeground="white",
            width=22,
            height=2,
            relief="flat",
            command=self.generate_report
        ).pack(pady=(0, 5))

    def format_time(self, total_seconds):
        total_seconds = int(total_seconds)

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def generate_report(self):
        # Screen time from main app start time
        total_seconds = int(time.time() - self.controller.app_start_time)
        running_time = self.format_time(total_seconds)
        today_minutes = total_seconds // 60

        if today_minutes < 60:
            usage_status = "Healthy usage"
        elif today_minutes < 120:
            usage_status = "Moderate usage"
        else:
            usage_status = "High usage"

        # Stress from Face ID
        stress = getattr(self.controller, "stress_level", "Not Scanned")

        # Reminder from Break Reminder page
        reminder = getattr(self.controller, "break_reminder_status", "No reminder set")

        report = (
            f"Live Screen Time : {running_time}\n"
            f"Today's Usage    : {today_minutes} mins\n"
            f"Usage Status     : {usage_status}\n\n"
            f"Stress Level     : {stress}\n"
            f"Break Reminder   : {reminder}\n\n"
            "Summary:\n"
            "Take regular breaks, stay hydrated, and continue monitoring your wellness."
        )

        self.report_text.config(text=report)