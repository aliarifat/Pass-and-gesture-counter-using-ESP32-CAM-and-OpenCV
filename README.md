# ✋ ESP32-CAM Pass & Gesture Counter using OpenCV & MediaPipe

Hello, we hope you’re doing fine. In this project, we build a **Pass Counter and Hand Gesture Counter** using the ESP32-CAM and Python-based image processing.

The ESP32-CAM captures images and sends them over Wi-Fi, while Python processes those images using **OpenCV**, **NumPy**, and **MediaPipe** to detect motion and hand gestures.

---

## 📌 Project Overview

This system performs two main tasks:

- 🔁 **Pass Counting** → Counts how many times a hand crosses a predefined line
- ✋ **Gesture Counting** → Detects and counts open-palm hand gestures

---

## 🧠 Technologies Used

- OpenCV (image processing)
- NumPy (array manipulation)
- MediaPipe (hand tracking & gesture detection)
- ESP32-CAM (image capture + web server)

---

## 📁 Project Structure
├── esp32_cam_basic.ino # ESP32-CAM firmware (image capture server)
├── pass_counter_esp32cam.py # Python script (pass + gesture detection)
└── README.md # Documentation

---

## ⚙️ System Architecture

### 1️⃣ ESP32-CAM Layer
- Captures live images
- Runs a web server
- Serves frames via `/cam-hi.jpg`
- Connects to Wi-Fi

---

### 2️⃣ Network Communication Layer
- Uses HTTP over Wi-Fi
- Sends one image per request
- Works on any local router

---

### 3️⃣ Python Processing Layer
- Fetches JPEG frames
- Decodes images using OpenCV
- Detects motion and contours
- Uses MediaPipe for hand tracking
- Counts finger states and gestures

---

### 4️⃣ Decision Layer
- Detects line crossing → increments pass counter
- Detects open palm → increments gesture counter
- Uses cooldown and state change logic to avoid false counts

---

### 5️⃣ Output Layer
- Displays annotated video feed
- Shows:
  - Counting line
  - Hand landmarks
  - Counters (pass + gesture)
- Exit using **ESC key**

---

## 🧰 Components Required

| Component | Quantity |
|----------|---------|
| ESP32-CAM Module | 1 |
| FTDI USB to Serial Converter | 1 |
| Jumper Wires | 5 |
| Micro USB Cable | 1 |

---

## 🔌 Circuit Connections

| ESP32-CAM | FTDI |
|----------|------|
| 5V | VCC |
| GND | GND |
| U0T | RX |
| U0R | TX |
| IO0 | GND (during upload only) |

⚠️ Set FTDI to **5V mode**

---

## 🔧 Setup Instructions

### 1️⃣ ESP32-CAM Setup
- Open `esp32_cam_basic.ino`
- Enter Wi-Fi credentials
- Upload code
- Open Serial Monitor
- Copy the IP address

---

### 2️⃣ Python Environment Setup

Install required libraries:

```bash
pip install opencv-python mediapipe numpy requests


```
## ▶️ Run the Project

1. Open the Python script:
   pass_counter_esp32cam.py


2. Locate the ESP32-CAM URL inside the script and update it:
```python
ESP32_URL = "http://<YOUR_ESP32_IP>/cam-hi.jpg"


```


Run the script:
```python
python pass_counter_esp32cam.py
```

# ✋ Features

*Real-time pass counting
Hand gesture recognition (open palm)
MediaPipe hand landmark detection
Stable tracking using cooldown logic
Live annotated video display
Lightweight ESP32 + Python architecture

---


---

# ✋ Testing

Power on the ESP32-CAM
Run the Python script
Perform the following actions:
Move your hand:
Above → Below the line → Pass counter increases
Show an open palm:
Gesture counter increases
Press ESC to exit the application

---


