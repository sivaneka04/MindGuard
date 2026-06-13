import tkinter as tk

# ===============================
# AI RESPONSE (SIMPLE + FRIENDLY)
# ===============================
def get_ai_response(text):
    text = text.lower()

    if "stress" in text or "tired" in text:
        return (
            "💙 I understand you're feeling a bit stressed. "
            "Try taking a short break, drink some water, and slow down your breathing. "
            "Even a few minutes can help you feel better."
        )

    elif "sad" in text:
        return (
            "💙 I'm sorry you're feeling this way. "
            "Maybe you can talk to someone you trust or take a short walk. "
            "You’re not alone in this."
        )

    elif "more" in text or "suggest" in text:
        return (
            "✨ You could also try listening to calming music, stretching your body, "
            "or writing down your thoughts. Small actions can really improve your mood."
        )

    elif "thank" in text:
        return (
            "💙 You're always welcome. I'm glad I could help. "
            "Take care of yourself 😊"
        )

    elif "hi" in text:
        return "🤖 Hi! I'm Nick AI. How are you feeling today?"

    else:
        return (
            "💙 I'm here for you. Tell me how you're feeling and I'll try to help."
        )


# ===============================
# OPEN CHAT WINDOW
# ===============================
def open_chat(parent):

    chat_win = tk.Toplevel(parent)
    chat_win.title("Nick AI")
    chat_win.geometry("350x500")
    chat_win.configure(bg="#F5F6FA")

    # Position bottom-right
    x = parent.winfo_rootx() + parent.winfo_width() - 370
    y = parent.winfo_rooty() + parent.winfo_height() - 550
    chat_win.geometry(f"+{x}+{y}")

    # HEADER
    header = tk.Frame(chat_win, bg="#6C63FF", height=50)
    header.pack(fill="x")

    tk.Label(
        header,
        text="🤖 Nick AI",
        bg="#6C63FF",
        fg="white",
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    # CHAT AREA
    chat_area = tk.Text(chat_win, bg="white", font=("Arial", 10))
    chat_area.pack(fill="both", expand=True, padx=10, pady=10)

    # INPUT
    input_frame = tk.Frame(chat_win, bg="#F5F6FA")
    input_frame.pack(fill="x", padx=10, pady=10)

    user_input = tk.Entry(input_frame)
    user_input.pack(side="left", fill="x", expand=True, padx=(0, 5))

    def send():
        msg = user_input.get()
        if not msg.strip():
            return

        chat_area.insert(tk.END, f"\n👤 {msg}\n")

        reply = get_ai_response(msg)

        chat_area.insert(tk.END, f"🤖 {reply}\n")
        chat_area.see(tk.END)

        user_input.delete(0, tk.END)

    tk.Button(
        input_frame,
        text="Send",
        command=send,
        bg="#6C63FF",
        fg="white"
    ).pack(side="right")