import tkinter as tk
import time

from login import LoginPage
from dashboard import DashboardPage
from screen_time import ScreenTimePage
from face_id import FaceIDPage
from break_reminder import BreakPage
from report import ReportPage



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("MindGuard")
        self.state("zoomed")

        self.app_start_time = time.time()
        self.stress_level = "Not Scanned"
        self.break_reminder_status = "No reminder set"

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        pages = (
            LoginPage,
            DashboardPage,
            ScreenTimePage,
            FaceIDPage,
            BreakPage,
            ReportPage

        )

        for Page in pages:
            name = Page.__name__
            frame = Page(container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, name):
        self.frames[name].tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()