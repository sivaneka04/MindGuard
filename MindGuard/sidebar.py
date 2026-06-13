import tkinter as tk
from tkinter import messagebox

# =========================
# GLOBAL DESIGN COLORS
# =========================
APP_BG = "#071739"        # dark navy background
SIDEBAR_BG = "#FFFFFF"    # white sidebar
MENU_BG = "#F1F5F9"       # light grey menu box
MENU_HOVER = "#E2E8F0"
CARD_BG = "#FFFFFF"       # white card
CARD_SHADOW = "#020617"

TEXT_COLOR = "#0F172A"    # dark navy text
SUB_TEXT = "#64748B"      # grey subtitle
TITLE_COLOR = "#FFFFFF"   # white title
ACCENT = "#2563EB"        # blue heading
GREEN = "#16A34A"
RED = "#DC2626"


class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=SIDEBAR_BG, width=260)

        self.controller = controller
        self.pack_propagate(False)

        # App title
        tk.Label(
            self,
            text="MindGuard",
            font=("Segoe UI", 24, "bold"),
            bg=SIDEBAR_BG,
            fg="#0284C7"
        ).pack(pady=(35, 4))

        tk.Label(
            self,
            text="Digital Wellness App",
            font=("Segoe UI", 10),
            bg=SIDEBAR_BG,
            fg=SUB_TEXT
        ).pack(pady=(0, 35))

        # Sidebar menu
        self.create_menu_button("⌂  Dashboard", "DashboardPage")
        self.create_menu_button("⏱  Screen Time", "ScreenTimePage")
        self.create_menu_button("☻  Face ID", "FaceIDPage")

        # IMPORTANT:
        # If your main.py uses another class name, change only this page name.
        self.create_menu_button("⏰  Break Reminder", "BreakPage")

        self.create_menu_button("▤  Report", "ReportPage")
        self.create_menu_button("▣  Logout", "LoginPage")

    def create_menu_button(self, text, page_name):
        btn = tk.Button(
            self,
            text=text,
            font=("Segoe UI", 12, "bold"),
            bg=MENU_BG,
            fg=TEXT_COLOR,
            activebackground=MENU_HOVER,
            activeforeground=TEXT_COLOR,
            bd=0,
            anchor="w",
            padx=25,
            pady=14,
            cursor="hand2",
            command=lambda p=page_name: self.go_to_page(p)
        )
        btn.pack(fill="x", padx=18, pady=7)

        btn.bind("<Enter>", lambda e: btn.config(bg=MENU_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=MENU_BG))

    def go_to_page(self, page_name):
        try:
            self.controller.show_frame(page_name)
        except KeyError:
            messagebox.showerror(
                "Page Error",
                f"Page '{page_name}' is not registered in main.py.\n\n"
                f"Check your main.py page list and make sure the class name matches."
            )
        except Exception as e:
            messagebox.showerror("Navigation Error", str(e))

