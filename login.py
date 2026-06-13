import tkinter as tk
import os
import sys
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0F172A")
        self.controller = controller

        main_frame = tk.Frame(self, bg="#0F172A")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # ===== LOGO =====
        img = Image.open(resource_path("logo.png")).convert("RGBA").resize((160, 160))

        mask = Image.new("L", (160, 160), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 160, 160), fill=255)
        img.putalpha(mask)

        self.logo_img = ImageTk.PhotoImage(img)

        tk.Label(main_frame, image=self.logo_img, bg="#0F172A").pack(pady=10)

        # ==q=== TITLE =====
        tk.Label(
            main_frame,
            text="MindGuard",
            font=("Segoe UI", 26, "bold"),
            fg="white",
            bg="#0F172A"
        ).pack()

        tk.Label(
            main_frame,
            text="Digital Wellness Login",
            font=("Segoe UI", 12),
            fg="#CBD5F5",
            bg="#0F172A"
        ).pack(pady=(0, 20))

        # ===== INPUT =====
        style = {
            "font": ("Segoe UI", 12),
            "bg": "#1E293B",
            "fg": "white",
            "insertbackground": "white",
            "relief": "flat",
            "width": 28
        }

        tk.Label(main_frame, text="Username", fg="#CBD5F5", bg="#0F172A").pack(anchor="w")
        self.user = tk.Entry(main_frame, **style)
        self.user.pack(pady=5, ipady=6)

        tk.Label(main_frame, text="Password", fg="#CBD5F5", bg="#0F172A").pack(anchor="w")
        self.pwd = tk.Entry(main_frame, show="*", **style)
        self.pwd.pack(pady=5, ipady=6)

        # ===== BUTTON =====
        tk.Button(
            main_frame,
            text="Login",
            command=self.login,
            bg="white",
            fg="#0F172A",
            font=("Segoe UI", 12, "bold"),
            padx=25,
            pady=8,
            relief="flat"
        ).pack(pady=15)

    def login(self):
        if self.user.get() == "admin" and self.pwd.get() == "admin":
            self.controller.show_frame("DashboardPage")
        else:
            messagebox.showerror("Error", "Invalid login")