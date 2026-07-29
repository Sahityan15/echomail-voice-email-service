# EchoMail: Voice-Driven Email Service for the Visually Challenged

EchoMail is a Python-based voice-driven email application designed to help visually challenged users manage emails independently using voice commands. The system integrates Speech Recognition, Text-to-Speech (TTS), SMTP, and IMAP technologies to provide a completely hands-free email experience, allowing users to compose, send, read, and delete emails without relying on a keyboard or mouse.

---

## 📌 Overview

Traditional email applications require visual interaction and manual typing, making them difficult for visually challenged individuals. EchoMail addresses this challenge by enabling users to interact with their email accounts entirely through voice commands.

The application authenticates users, recognizes spoken commands, converts speech into text, performs email operations, and provides spoken feedback through Text-to-Speech technology, creating an accessible and user-friendly communication platform.

---

## ✨ Features

- Voice-based user authentication
- Voice-controlled email composition
- Send emails using speech commands
- Read received emails aloud
- Delete emails using voice confirmation
- Text-to-Speech feedback for every action
- Speech Recognition for natural voice interaction
- Gmail SMTP and IMAP integration
- Hands-free email management
- Designed for visually challenged users

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Application Development |
| SpeechRecognition | Voice Command Recognition |
| pyttsx3 | Text-to-Speech Output |
| SMTP | Sending Emails |
| IMAP | Reading Emails |
| JSON | User Credential Storage |

---

## 📂 Project Structure

```text
echomail-voice-email-service/
│
├── main.py
├── next.py
├── users.json
├── requirements.txt
├── EchoMail Demo.mp4
├── README.md
├── LICENSE
└── .gitignore
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/Sahityan15/echomail-voice-email-service.git
```

### Navigate to the project

```bash
cd echomail-voice-email-service
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python main.py
```

---

## ▶️ Usage

1. Launch the application.
2. Register a new account or log in using voice commands.
3. Choose an email operation.
4. Speak the required information such as recipient, subject, and message.
5. Listen to received emails through Text-to-Speech.
6. Delete emails using voice confirmation when required.

---

## 🎥 Demo Video

A demonstration video of the application is included in this repository.

**File:** `EchoMail Demo.mp4`

---

## 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for more information.
