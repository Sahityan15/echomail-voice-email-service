import json
import os
import speech_recognition as sr
import subprocess
import pyttsx3
import sys

users_file = "users.json"

# Load users
if os.path.exists(users_file):
    with open(users_file, "r") as f:
        users = json.load(f)
else:
    users = {}


# Text-to-Speech
def speak(text):
    print("System:", text)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Speech Recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio).lower()
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand. Please try again.")
        except sr.RequestError:
            speak("Check your internet connection.")
    return None


# Extract Keywords
def extract_keyword(text, phrase):
    if text and phrase in text:
        words = text.split()
        index = words.index(phrase.split()[-1])
        return words[index + 1] if index + 1 < len(words) else None
    return None


# Sign In
def sign_in():
    while True:
        speak("Say 'My name is' followed by your name:")
        text = recognize_speech()
        name = extract_keyword(text, "my name is")

        if not name or name.strip() == "":
            speak("Could not detect a valid name. Try again.")
            continue

        if name in users:
            speak("User already exists! Try logging in.")
            return

        speak("Say 'my password is' followed by your password:")
        text = recognize_speech()
        password = extract_keyword(text, "my password is")

        if not password or password.strip() == "":
            speak("Could not detect a valid password. Try again.")
            continue

        users[name] = str(password)  # Store as a string
        with open(users_file, "w") as f:
            json.dump(users, f)

        speak("Sign-in successful! You can now log in.")
        break


# Login
def log_in():
    speak("Say 'My name is' followed by your name:")
    text = recognize_speech()
    name = extract_keyword(text, "my name is")

    if not name or name.strip() == "":
        speak("Invalid name. Please try again.")
        return

    # Check if name exists in users.json
    if name not in users:
        speak("User not found. Please sign in first.")
        return

    stored_password = str(users[name])  # Get the correct password
    attempts = 5  # Allow up to 5 attempts for password

    while attempts > 0:
        speak("Say 'my password is' followed by your password:")
        text = recognize_speech()
        password = extract_keyword(text, "my password is")

        if not password or password.strip() == "":
            speak("Invalid password format. Please try again.")
            continue

        entered_password = str(password)  # Convert to string for comparison
        print(f"DEBUG: Name: {name}, Entered Password: {entered_password}, Stored Password: {stored_password}")

        if entered_password == stored_password:
            speak("Welcome! Logging you in...")
            subprocess.run([sys.executable, "next.py"])
            sys.exit()
        else:
            attempts -= 1
            speak(f"Incorrect password! {attempts} attempts remaining.")

    speak("Too many failed attempts. Try again later.")


# Main Function
def main():
    while True:
        speak("Say 'sign in' to register or 'log in' to continue:")
        choice = recognize_speech()
        if choice:
            if "sign in" in choice:
                sign_in()
            elif "login" in choice:
                log_in()
            else:
                speak("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
