import tkinter as tk
from tkinter import messagebox, filedialog
import cv2
import requests
import os

from sidebar import Sidebar
from data import report_data

APP_BG = "#071739"        # dark navy background
CARD_BG = "#FFFFFF"       # white glass box
CARD_SHADOW = "#020617"   # dark shadow
TITLE_COLOR = "#FFFFFF"   # white title
TEXT_COLOR = "#0F172A"    # dark text inside box
SUB_TEXT = "#CBD5E1"      # subtitle outside box
ACCENT = "#2563EB"        # blue heading inside box
GREEN = "#16A34A"
RED = "#DC2626"

API_KEY = "API KEY"
API_SECRET = "API SECRET"
FACE_API_URL = "https://api-us.faceplusplus.com/facepp/v3/detect"


class FaceIDPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=APP_BG)
        self.controller = controller

        Sidebar(self, controller).pack(side="left", fill="y")

        # MAIN CONTENT
        content = tk.Frame(self, bg=APP_BG)
        content.pack(side="left", expand=True, fill="both")

        # PAGE TITLE
        tk.Label(
            content,
            text="Face ID Scanner",
            font=("Segoe UI", 30, "bold"),
            fg=TITLE_COLOR,
            bg=APP_BG
        ).place(x=60, y=35)

        tk.Label(
            content,
            text="Use live scan or upload a face image for stress analysis.",
            font=("Segoe UI", 13),
            fg=SUB_TEXT,
            bg=APP_BG
        ).place(x=65, y=90)

        # SHADOW
        shadow = tk.Frame(content, bg=CARD_SHADOW)
        shadow.place(x=132, y=155, width=780, height=470)

        # WHITE GLASS BOX
        self.card = tk.Frame(
            content,
            bg=CARD_BG,
            highlightbackground="#E2E8F0",
            highlightthickness=1
        )
        self.card.place(x=120, y=145, width=780, height=470)

        # CARD TITLE
        tk.Label(
            self.card,
            text="Facial Stress Analysis",
            font=("Segoe UI", 22, "bold"),
            fg=ACCENT,
            bg=CARD_BG
        ).place(relx=0.5, y=45, anchor="center")

        tk.Label(
            self.card,
            text="The system checks face quality, eye cues and face position before estimating stress.",
            font=("Segoe UI", 11),
            fg="#475569",
            bg=CARD_BG,
            wraplength=650,
            justify="center"
        ).place(relx=0.5, y=90, anchor="center")

        # STATUS
        self.scan_status_label = tk.Label(
            self.card,
            text="Scan Status: Ready",
            font=("Segoe UI", 14, "bold"),
            fg=TEXT_COLOR,
            bg=CARD_BG
        )
        self.scan_status_label.place(relx=0.5, y=145, anchor="center")

        # STRESS LEVEL
        self.stress_label = tk.Label(
            self.card,
            text="Stress Level: -",
            font=("Segoe UI", 18, "bold"),
            fg=TEXT_COLOR,
            bg=CARD_BG
        )
        self.stress_label.place(relx=0.5, y=200, anchor="center")

        # FACIAL CUES
        self.cues_label = tk.Label(
            self.card,
            text="Facial Cues:\nFace Quality: -\nEyes: -\nPosition: -",
            font=("Segoe UI", 13),
            fg="#475569",
            bg=CARD_BG,
            justify="center"
        )
        self.cues_label.place(relx=0.5, y=270, anchor="center")

        # SYSTEM MESSAGE
        self.message_label = tk.Label(
            self.card,
            text="System Message: Ready",
            font=("Segoe UI", 12),
            fg="#475569",
            bg=CARD_BG,
            wraplength=650,
            justify="center"
        )
        self.message_label.place(relx=0.5, y=350, anchor="center")

        # BUTTONS
        self.live_scan_btn = tk.Button(
            self.card,
            text="Start Live Face Scan",
            bg=GREEN,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            width=20,
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.start_scan
        )
        self.live_scan_btn.place(x=190, y=395)

        self.upload_btn = tk.Button(
            self.card,
            text="Upload Face Image",
            bg=ACCENT,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            width=20,
            height=2,
            relief="flat",
            cursor="hand2",
            command=self.upload_face_image
        )
        self.upload_btn.place(x=410, y=395)

    def start_scan(self):

        confirm = messagebox.askyesno(
            "Camera Permission",
            "Allow camera access for face scanning?"
        )

        if not confirm:
            return

        self.reset_display()

        self.scan_status_label.config(
            text="Scan Status: Live Camera Active"
        )

        self.message_label.config(
            text="System Message: Press 'S' to scan face or 'Q' to quit."
        )

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            self.message_label.config(
                text="System Message: Webcam not detected"
            )

            return

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            cv2.imshow("MindGuard Live Scan", frame)

            key = cv2.waitKey(1)

            # PRESS S TO SCAN
            if key == ord("s"):

                temp_image = "live_capture.jpg"

                cv2.imwrite(temp_image, frame)

                cap.release()
                cv2.destroyAllWindows()

                self.scan_status_label.config(
                    text="Scan Status: Processing Live Scan"
                )

                self.analyze_frame(
                    temp_image,
                    "Centered",
                    "Good",
                    "Eyes Open"
                )

                return

            # PRESS Q TO QUIT
            elif key == ord("q"):

                cap.release()
                cv2.destroyAllWindows()

                self.scan_status_label.config(
                    text="Scan Status: Cancelled"
                )

                self.message_label.config(
                    text="System Message: Live scan cancelled."
                )

                return

    def upload_face_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Face Image",
            filetypes=(
                ("Image Files", "*.jpg *.jpeg *.png"),
                ("All Files", "*.*")
            )
        )

        if not file_path:
            self.show_failed("No image selected.")
            return

        self.reset_display()
        self.scan_status_label.config(text="Scan Status: Processing Uploaded Image")
        self.message_label.config(text="System Message: Analyzing uploaded image...")

        image = cv2.imread(file_path)
        if image is None:
            self.show_failed("Unable to read the selected image.")
            return

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_eye.xml"
        )

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) == 0:
            self.show_failed("No face detected in uploaded image.")
            return

        if len(faces) > 1:
            self.show_failed("Multiple faces detected in uploaded image.")
            return

        (x, y, w, h) = faces[0]
        face_img = image[y:y + h, x:x + w]
        gray_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(gray_face, 1.1, 5)

        frame_width = image.shape[1]
        center_x = x + w // 2

        if abs(center_x - frame_width // 2) < frame_width * 0.15:
            face_position = "Centered"
        else:
            face_position = "Not Centered"

        if w >= 120 and h >= 120:
            face_quality = "Clear"
        else:
            face_quality = "Unclear"

        if len(eyes) >= 1:
            eyes_cue = "Normal"
        else:
            eyes_cue = "Tired"

        self.analyze_frame(file_path, face_position, face_quality, eyes_cue)

    def analyze_frame(
            self,
            image,
            face_position,
            face_quality,
            eyes_cue
    ):

        api_result = self.detect_emotion_with_api(image)

        print("API RESULT:", api_result)

        dominant_emotion = api_result["dominant_emotion"]
        emotion_scores = api_result["emotion_scores"]

        stress, message = self.map_emotion_to_stress(
            dominant_emotion,
            emotion_scores,
            face_position,
            face_quality,
            eyes_cue
        )

        self.controller.stress_level = stress

        if dominant_emotion == "Unknown":

            self.scan_status_label.config(
                text="Scan Status: Failed"
            )

        else:

            self.scan_status_label.config(
                text="Scan Status: Scan Successful"
            )

        self.stress_label.config(
            text=f"Stress Level: {stress}"
        )

        self.cues_label.config(
            text=(
                "Facial Cues:\n"
                f"Face Quality: {face_quality}\n"
                f"Eyes: {eyes_cue}\n"
                f"Position: {face_position}"
            )
        )

        self.message_label.config(
            text=f"System Message: {message}"
        )

    def detect_emotion_with_api(self, image_path):

        try:

            with open(image_path, "rb") as f:

                response = requests.post(
                    FACE_API_URL,
                    data={
                        "api_key": API_KEY,
                        "api_secret": API_SECRET,
                        "return_attributes": "emotion"
                    },
                    files={
                        "image_file": f
                    }
                )

            result = response.json()

            print("DEBUG:", result)

            if "faces" in result and len(result["faces"]) > 0:
                emotions = result["faces"][0]["attributes"]["emotion"]

                dominant_emotion = max(
                    emotions,
                    key=emotions.get
                )

                return {
                    "dominant_emotion": dominant_emotion,
                    "emotion_scores": emotions
                }

            return {
                "dominant_emotion": "Unknown",
                "emotion_scores": {}
            }

        except Exception as e:

            print("ERROR:", e)

            return {
                "dominant_emotion": "Unknown",
                "emotion_scores": {}
            }

    def map_emotion_to_stress(self, dominant_emotion, emotion_scores, face_position, face_quality, eyes_cue):
        e = dominant_emotion.lower()

        happiness = emotion_scores.get("happiness", 0)
        sadness = emotion_scores.get("sadness", 0)
        fear = emotion_scores.get("fear", 0)
        disgust = emotion_scores.get("disgust", 0)
        anger = emotion_scores.get("anger", 0)
        neutral = emotion_scores.get("neutral", 0)

        if e == "unknown":
            return "Moderate", "Emotion could not be detected clearly. Please try again."

        if face_quality == "Unclear":
            return "Moderate", "Image quality is unclear. Please try a clearer image."

        if face_position != "Centered":
            return "Moderate", "Please align your face properly."

        if happiness >= 60:
            return "Low", "You appear relaxed 😊."

        if sadness >= 20 or fear >= 20 or disgust >= 15:
            return "High", "Signs of strain detected. Please take a short break 💙."

        if neutral >= 50 and (sadness >= 2 or fear >= 1 or anger >= 2):
            return "High", "There are signs of tiredness or strain. Please take some rest 💙."

        if anger >= 10:
            return "Moderate", "Some strain is present. Please monitor your wellness🌿."

        if eyes_cue == "Tired":
            return "Moderate", "You may look tired. Please take some rest 💙."

        return "Moderate", "Please continue to monitor your screen usage🌿."

    def reset_display(self):
        self.stress_label.config(text="Stress Level: -", fg=TEXT_COLOR)
        self.cues_label.config(
            text="Facial Cues:\nFace Quality: -\nEyes: -\nPosition: -"
        )
        self.scan_status_label.config(text="Scan Status: Ready")
        self.message_label.config(text="System Message: Ready")

    def show_failed(self, msg):
        self.scan_status_label.config(text="Scan Status: Scan Failed")
        self.stress_label.config(text="Stress Level: -", fg="#64748B")
        self.cues_label.config(
            text="Facial Cues:\nFace Quality: -\nEyes: -\nPosition: -"
        )
        self.message_label.config(text=f"System Message: {msg}")