# 🖐️ Smart Hand Gesture Controller

Control your mouse with hand gestures using your webcam — no hardware needed!

Built with Python, OpenCV, and MediaPipe.

---

## 📸 Demo

| Gesture | Action |
|---|---|
| ☝️ Move index finger | Move the mouse cursor |
| 🤏 Pinch thumb + index | Left click |
| ⌨️ Press `q` | Quit the app |

---

## 🧰 Tech Stack

- **Python 3.11**
- **OpenCV** — webcam capture & video display
- **MediaPipe** — real-time hand landmark detection (21 points)
- **PyAutoGUI** — mouse & keyboard control
- **NumPy** — math calculations (interpolation, distance)

---

## 📁 Project Structure

```
smart-hand-gesture/
├── gesture_controller.py   # Main script
├── requirements.txt        # Dependencies
└── README.md               # This file
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/smart-hand-gesture.git
cd smart-hand-gesture
```

### 2. Make sure you have Python 3.11

```bash
py -3.11 --version
```

> Download Python 3.11 at https://www.python.org/downloads/release/python-3119/

### 3. Install dependencies

```bash
py -3.11 -m pip install -r requirements.txt
```

---

## 🚀 Usage

```bash
py -3.11 gesture_controller.py
```

A window will open showing your webcam feed with hand landmarks drawn in real time.

---

## 🔧 Configuration

You can tweak these variables in `gesture_controller.py`:

| Variable | Default | Description |
|---|---|---|
| `smoothing` | `5` | Mouse smoothing factor. Higher = smoother, less reactive |
| `min_detection_confidence` | `0.7` | Minimum confidence to detect a hand |
| `min_tracking_confidence` | `0.5` | Minimum confidence to keep tracking |
| `distance < 0.05` | `0.05` | Pinch threshold for click detection |

---

## 🐛 Troubleshooting

**`ModuleNotFoundError: No module named 'mediapipe'`**
```bash
py -3.11 -m pip install mediapipe==0.10.9
```

**`Error: Could not open camera`**
- Make sure your webcam is connected and not used by another app
- Try changing `VideoCapture(0)` to `VideoCapture(1)`

**Mouse moves but no click detected**
- Bring thumb and index finger closer together
- Lower the threshold: change `0.05` to `0.07`

---

## 📚 How It Works

1. Webcam captures frames in real time
2. MediaPipe detects 21 hand landmarks
3. Landmark `[8]` (index fingertip) controls mouse position
4. `np.interp` maps camera coordinates to screen coordinates
5. Smoothing formula prevents cursor jitter
6. Euclidean distance between `[4]` (thumb) and `[8]` triggers click

---

## 🌱 Future Improvements

- [ ] Double-click gesture
- [ ] Scroll with two fingers
- [ ] Right-click gesture
- [ ] Drag & drop support
- [ ] Gesture customization config file

---

## 👩‍💻 Author

Made by **Nour Faker** — 1st year Computer Engineering student  
Passionate about Computer Vision & AI 🤖

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
