import tkinter as tk
from tkinter import Button, Label, Frame
from PIL import Image, ImageTk
import cv2

class WebcamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Capture & Processing")
        self.root.geometry("900x700")
        self.root.configure(bg="#2c3e50")

        # Header Frame
        header = Frame(root, bg="#34495e", height=60)
        header.pack(fill="x")
        header_label = Label(
            header, text="Webcam Image Capture & Processing",
            bg="#34495e", fg="#ecf0f1", font=("Helvetica", 24, "bold")
        )
        header_label.pack(pady=10)

        # Image Display Frame
        self.image_frame = Frame(root, bg="#2c3e50")
        self.image_frame.pack(pady=30)
        self.label = Label(self.image_frame, bg="#2c3e50")
        self.label.pack()

        # Button Frame
        button_frame = Frame(root, bg="#2c3e50")
        button_frame.pack(pady=20)

        self.capture_button = Button(
            button_frame, text="Capture Image", command=self.capture_image,
            bg="#27ae60", fg="#fff", font=("Helvetica", 14, "bold"),
            activebackground="#2ecc71", width=16, height=2, borderwidth=0
        )
        self.capture_button.grid(row=0, column=0, padx=15)

        self.process_button = Button(
            button_frame, text="Process Image", command=self.process_image,
            bg="#2980b9", fg="#fff", font=("Helvetica", 14, "bold"),
            activebackground="#3498db", width=16, height=2, borderwidth=0
        )
        self.process_button.grid(row=0, column=1, padx=15)

        self.status_label = Label(
            root, text="", bg="#2c3e50", fg="#f1c40f", font=("Helvetica", 12)
        )
        self.status_label.pack(pady=10)

        self.video_capture = cv2.VideoCapture(0)
        self.current_image = None  # PIL image

        self.update_video_stream()

    def update_video_stream(self):
        ret, frame = self.video_capture.read()
        if ret:
            # Flip the image vertically if needed
            frame = cv2.flip(frame, 1)  # 1 for horizontal, 0 for vertical, -1 for both
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=self.current_image.resize((500, 350)))
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
        self.root.after(20, self.update_video_stream)

    def capture_image(self):
        if self.current_image:
            self.current_image.save("captured_image.jpg")
            self.status_label.config(text="Image saved as captured_image.jpg", fg="#2ecc71")

    def process_image(self):
        if self.current_image:
            # Example: Convert to grayscale
            gray_image = self.current_image.convert("L")
            gray_image.save("processed_image.jpg")
            imgtk = ImageTk.PhotoImage(image=gray_image.resize((700, 500)))
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
            self.status_label.config(text="Processed image saved as processed_image.jpg", fg="#3498db")

    def __del__(self):
        if self.video_capture.isOpened():
            self.video_capture.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = WebcamApp(root)
    root.mainloop()
