import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import RPi.GPIO as GPIO
import threading

FAN_PIN = 8
GPIO.setmode(GPIO.BOARD)
GPIO.setup(FAN_PIN, GPIO.OUT)
fan_pwm = GPIO.PWM(FAN_PIN, 1000)
fan_pwm.start(0)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

root = tk.Tk()
root.title('Face Detection and Fan Control')
root.geometry('1000x800')

label = tk.Label(root)
label.pack()

zoom_var = tk.DoubleVar()
zoom_var.set(1.0)

def control_fan(area):
    duty_cycle = min(100, area)
    fan_pwm.ChangeDutyCycle(duty_cycle)

def update_frame():
    ret, frame = cap.read()
    if not ret:
        print("Camera not found")
        return
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        area = w * h
        text = f"Area: {area} in pixels"
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, text, (x, y - 10), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        control_fan(area)
    
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo
    
    elapsed_time = int((cv2.getTickCount() - start_time) / cv2.getTickFrequency() * 1000)
    delay = max(1, 30 - elapsed_time)
    root.after(delay, update_frame)

def start_feed():
    global start_time
    start_time = cv2.getTickCount()
    update_frame()

def change_camera(camera_index):
    global cap
    cap.release()
    cap = cv2.VideoCapture(camera_index)
    start_feed()

def toggle_mode():
    pass

start_button = ttk.Button(root, text="Start Camera", command=start_feed)
start_button.pack()

toggle_button = ttk.Button(root, text="Toggle Mode", command=toggle_mode)
toggle_button.pack()

menubar = tk.Menu(root)
camera_menu = tk.Menu(menubar, tearoff=0)
camera_menu.add_radiobutton(label="Camera 0", variable=0, command=lambda: change_camera(0))
camera_menu.add_radiobutton(label="Camera 1", variable=1, command=lambda: change_camera(1))

zoom_menu = tk.Menu(menubar, tearoff=0)
zoom_menu.add_radiobutton(label="0.5x", variable=zoom_var, value=0.5)
zoom_menu.add_radiobutton(label="1.0x", variable=zoom_var, value=1.0)
zoom_menu.add_radiobutton(label="1.5x", variable=zoom_var, value=1.5)
zoom_menu.add_radiobutton(label="2.0x", variable=zoom_var, value=2.0)

menubar.add_cascade(label="Camera", menu=camera_menu)
menubar.add_cascade(label="Zoom", menu=zoom_menu)
root.config(menu=menubar)

root.mainloop()

cap.release()
cv2.destroyAllWindows()
fan_pwm.stop()
GPIO.cleanup()
