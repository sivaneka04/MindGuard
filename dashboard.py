import tkinter as tk
import time
from tkinter import messagebox
from sidebar import Sidebar, APP_BG, CARD_BG, TEXT_COLOR, SUB_TEXT, ACCENT, GREEN
from data import report_data, get_screen_time_seconds


def format_time(seconds):
    seconds = int(seconds)
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hrs:02d}:{mins:02d}:{secs:02d}"


class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=APP_BG)

        self.controller = controller

        Sidebar(self, controller).pack(side="left", fill="y")

        self.content = tk.Frame(self, bg=APP_BG)
        self.content.pack(side="left", expand=True, fill="both", padx=35, pady=18)

        tk.Label(
            self.content,
            text="Dashboard",
            font=("Segoe UI", 26, "bold"),
            bg=APP_BG,
            fg="white"
        ).pack(anchor="w")

        tk.Label(
            self.content,
            text="Monitor your screen time, stress level and wellness activity.",
            font=("Segoe UI", 12),
            bg=APP_BG,
            fg="#CBD5E1"
        ).pack(anchor="w", pady=(2, 14))

        self.card_area = tk.Frame(self.content, bg=APP_BG)
        self.card_area.pack(anchor="center")

        self.screen_time_value = None
        self.today_usage_value = None
        self.usage_status_value = None
        self.face_stress_value = None
        self.reminder_value = None
        self.report_screen_value = None
        self.report_stress_value = None

        self.create_dashboard_cards()

        # ================= CHATBOT BUTTON =================
        # ================= CHATBOT BUTTON =================
        self.chat_btn = tk.Button(
            self.content,
            text="🤖  Chat with Nick",
            font=("Segoe UI", 12, "bold"),
            bg="#FFFFFF",
            fg="#0F172A",
            activebackground="#E2E8F0",
            activeforeground="#0F172A",
            bd=0,
            cursor="hand2",
            command=self.open_chatbot
        )
        self.chat_btn.pack(anchor="e", pady=(18, 0), padx=(0, 40))


        self.update_dashboard()

    def create_card(self, parent, title, row, col):
        shadow = tk.Frame(parent, bg="#020617")
        shadow.grid(row=row, column=col, padx=14, pady=12)

        card = tk.Frame(
            shadow,
            bg=CARD_BG,
            width=380,
            height=175,
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        card.pack(padx=(0, 6), pady=(0, 6))
        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 15, "bold"),
            bg=CARD_BG,
            fg=TEXT_COLOR
        ).pack(pady=(14, 6))

        return card

    def create_dashboard_cards(self):
        # Screen Time Card
        screen_card = self.create_card(self.card_area, "Screen Time", 0, 0)

        self.screen_time_value = tk.Label(
            screen_card,
            text="00:00:00",
            font=("Segoe UI", 17, "bold"),
            bg=CARD_BG,
            fg=TEXT_COLOR
        )
        self.screen_time_value.pack(pady=2)

        self.today_usage_value = tk.Label(
            screen_card,
            text="Today: 0 mins",
            font=("Segoe UI", 11),
            bg=CARD_BG,
            fg=SUB_TEXT
        )
        self.today_usage_value.pack(pady=2)

        self.usage_status_value = tk.Label(
            screen_card,
            text="Healthy usage",
            font=("Segoe UI", 14, "bold"),
            bg=CARD_BG,
            fg=GREEN
        )
        self.usage_status_value.pack(pady=2)

        # Face ID Card
        face_card = self.create_card(self.card_area, "Face ID", 0, 1)

        tk.Label(
            face_card,
            text="Stress Level:",
            font=("Segoe UI", 13, "bold"),
            bg=CARD_BG,
            fg=TEXT_COLOR
        ).pack(pady=(12, 2))

        self.face_stress_value = tk.Label(
            face_card,
            text="Not Scanned",
            font=("Segoe UI", 15, "bold"),
            bg=CARD_BG,
            fg=TEXT_COLOR
        )
        self.face_stress_value.pack()

        # Break Reminder Card
        break_card = self.create_card(self.card_area, "Break Reminder", 1, 0)

        self.reminder_value = tk.Label(
            break_card,
            text="No reminder set",
            font=("Segoe UI", 14, "bold"),
            bg=CARD_BG,
            fg=TEXT_COLOR
        )
        self.reminder_value.pack(pady=(12, 5))

        tk.Label(
            break_card,
            text="Stay hydrated 💧",
            font=("Segoe UI", 12, "bold"),
            bg=CARD_BG,
            fg=TEXT_COLOR
        ).pack()

        # Report Card
        report_card = self.create_card(self.card_area, "Overall Report", 1, 1)

        self.report_screen_value = tk.Label(
            report_card,
            text="Screen: 0 mins",
            font=("Segoe UI", 13, "bold"),
            bg=CARD_BG,
            fg=TEXT_COLOR
        )
        self.report_screen_value.pack(pady=(14, 3))

        self.report_stress_value = tk.Label(
            report_card,
            text="Stress: Not Scanned",
            font=("Segoe UI", 13, "bold"),
            bg=CARD_BG,
            fg=TEXT_COLOR
        )
        self.report_stress_value.pack()

    def update_dashboard(self):
        total_seconds = get_screen_time_seconds()
        running_time = format_time(total_seconds)
        today_minutes = total_seconds // 60

        if today_minutes < 60:
            usage_status = "Healthy usage"
            usage_color = GREEN
        elif today_minutes < 120:
            usage_status = "Moderate usage"
            usage_color = "#F59E0B"
        else:
            usage_status = "High usage"
            usage_color = "#DC2626"

        stress = report_data.get("stress_level", "Not Scanned")
        reminder = report_data.get("reminder_status", "No reminder set")

        self.screen_time_value.config(text=running_time)
        self.today_usage_value.config(text=f"Today: {today_minutes} mins")
        self.usage_status_value.config(text=usage_status, fg=usage_color)

        self.face_stress_value.config(text=stress)

        self.reminder_value.config(text=reminder)

        self.report_screen_value.config(text=f"Screen: {today_minutes} mins")
        self.report_stress_value.config(text=f"Stress: {stress}")

        self.after(1000, self.update_dashboard)
    def open_chatbot(self):
        chat_window = tk.Toplevel(self)
        chat_window.title("Nick - MindGuard Assistant")
        chat_window.geometry("520x620")
        chat_window.configure(bg="#071739")
        chat_window.resizable(False, False)

        tk.Label(
            chat_window,
            text="Nick Assistant",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#071739"
        ).pack(pady=(20, 5))

        tk.Label(
            chat_window,
            text="Ask me about screen time, stress, or break reminders.",
            font=("Segoe UI", 10),
            fg="#CBD5E1",
            bg="#071739"
        ).pack(pady=(0, 15))

        chat_box = tk.Text(
            chat_window,
            font=("Segoe UI", 11),
            bg="white",
            fg="#0F172A",
            wrap="word",
            bd=0,
            padx=12,
            pady=12
        )
        chat_box.pack(padx=20, pady=10, fill="both", expand=False)
        chat_box.config(height=18)

        chat_box.insert(
            "end",
            "Nick: Hi 😊 I am Nick. How are you feeling today?\n\n"
        )
        chat_box.config(state="disabled")

        input_frame = tk.Frame(chat_window, bg="#071739")
        input_frame.pack(fill="x", padx=20, pady=(5, 20))

        user_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            bg="white",
            fg="#0F172A",
            bd=0
        )
        user_entry.pack(side="left", fill="x", expand=True, ipady=10)

        def send_message():
            user_msg = user_entry.get().strip()

            if user_msg == "":
                return

            chat_box.config(state="normal")
            chat_box.insert("end", f"You: {user_msg}\n")

            reply = self.nick_reply(user_msg)

            chat_box.insert("end", f"Nick: {reply}\n\n")
            chat_box.config(state="disabled")
            chat_box.see("end")

            user_entry.delete(0, "end")

        send_btn = tk.Button(
            input_frame,
            text="Send",
            font=("Segoe UI", 11, "bold"),
            bg="#2563EB",
            fg="white",
            bd=0,
            width=8,
            command=send_message
        )
        send_btn.pack(side="right", padx=(8, 0), ipady=9)

        user_entry.bind("<Return>", lambda event: send_message())
        user_entry.focus()

    def nick_reply(self, message):
        msg = message.lower().strip()

        if msg in ["hi", "hello", "hey", "hii", "hai"]:
            return (
                "Hi 😊 How are you feeling today?\n"
                "If you feel tired, try resting your eyes for a few minutes, drink some water, "
                "and take a short break from the screen."
            )

        elif "how are you" in msg:
            return (
                "I am doing good 😊 Thank you for asking.\n"
                "I am here to help you with your screen time, stress level, and wellness reminders."
            )

        elif "feel tired" in msg or "tired" in msg or "sleepy" in msg:
            return (
                "You may need a short rest. Try looking away from the screen for 20 seconds, "
                "stretch your body, and drink some water.\n"
                "If you still feel tired, take a longer break before continuing your work."
            )

        elif "stress" in msg or "stressed" in msg or "pressure" in msg:
            return (
                "Stress can happen when you use the screen for too long or focus for many hours.\n"
                "Try closing your eyes for a moment, breathe slowly, relax your shoulders, "
                "and take a short walk if possible."
            )

        elif "screen" in msg or "screen time" in msg or "time" in msg:
            return (
                "Your screen time is monitored to help you understand your usage.\n"
                "If your screen time is increasing, try using the 20-20-20 rule: every 20 minutes, "
                "look at something 20 feet away for 20 seconds."
            )

        elif "break" in msg or "reminder" in msg:
            return (
                "Break reminders are useful to protect your eyes and reduce tiredness.\n"
                "You can set a reminder for a suitable time, like every 30 minutes or 1 hour, "
                "then take a short break when it reminds you."
            )

        elif "report" in msg or "summary" in msg:
            return (
                "The report shows your screen time, stress level, and reminder status.\n"
                "You can use it to understand your digital wellness and improve your daily habits."
            )

        elif "more" in msg or "suggestion" in msg or "advice" in msg:
            return (
                "Here are some simple wellness suggestions:\n"
                "1. Drink enough water.\n"
                "2. Take short breaks often.\n"
                "3. Stretch your neck, hands, and shoulders.\n"
                "4. Avoid using the screen continuously for many hours.\n"
                "5. Sleep well and rest your eyes when needed.\n"
                "Small breaks can help you feel better and stay focused."
            )

        elif "sad" in msg or "not good" in msg or "bad" in msg or "feel" in msg or "lost" in msg:
            return (
                "I am sorry you are feeling that way 💙\n"
                "Try to take a small break, drink water, and do something calming for a few minutes. "
                "You can also talk to someone you trust if you feel low."
            )

        elif "happy" in msg or "good" in msg or "fine" in msg or "excited" in msg:
            return (
                "That is nice to hear 😊\n"
                "Keep maintaining healthy screen habits. Remember to take breaks and stay hydrated."
            )

        elif "thank" in msg or "thanks" in msg or "tq" in msg:
            return (
                "You are welcome 😊\n"
                "Take care of yourself, rest your eyes, and have a good day."
            )

        elif "bye" in msg or "goodbye" in msg or "papai" in msg:
            return (
                "Bye 😊 Take care.\n"
                "Remember to rest your eyes and take short breaks when using the screen."
            )

        else:
            return (
                "I am Nick, your MindGuard assistant 😊\n"
                "You can ask me about screen time, stress, break reminders, reports, or wellness suggestions."
            )