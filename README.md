# 🤟 SignSpeak – Real-Time Sign Language Recognition

A real-time sign language recognition system using Python backend and a custom image dataset. The app detects hand signs from the webcam and converts them to text, enabling smooth communication for individuals with hearing or speech difficulties.

---

## 📊 Accuracy

🎯 Achieved **84% accuracy** on a custom image dataset trained for recognizing alphabetic hand signs.

---

## 💡 Features

- 🔤 Real-time recognition of alphabet hand signs
- 🧠 Custom-trained model using own image dataset
- 📈 Accuracy score: 84%
- 🖥️ Web interface using HTML, CSS, and JavaScript
- 🐍 Python backend for ML inference and logic

---

## 🛠️ Technologies Used

| Area         | Tools                           |
|--------------|----------------------------------|
| Backend      | Python, Flask                   |
| Frontend     | HTML, CSS, JavaScript           |
| ML Libraries | OpenCV, TensorFlow, MediaPipe   |
| Dataset      | Custom-collected hand sign images |

---

## 🧠 How it Works

1. User starts webcam from browser interface
2. OpenCV captures frames and detects hand region
3. Trained ML model classifies the hand sign
4. The corresponding letter is displayed on the web page

---

## 🖥️ Screenshots

> Add screenshots or demo GIFs here to visualize your work

---

## 🚀 Getting Started

```bash
git clone https://github.com/Abozied448/sign-language-app.git
cd signspeak
pip install -r requirements.txt
python app.py


