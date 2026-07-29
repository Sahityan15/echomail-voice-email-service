import smtplib
import speech_recognition as sr
import pyttsx3
import imaplib
import email
from email.message import EmailMessage
from email.header import decode_header

# Initialize Speech Recognition & Text-to-Speech
listener = sr.Recognizer()
engine = pyttsx3.init()

# Email credentials
sender_email = 'darshanar227@gmail.com'  # Update sender email
sender_password = 'ukfd hxuw gcip vnlu'  # Replace with app-specific password

# Email Contacts
email_list = {
    'guru': 'ardarhan332@gmail.com',
    'sonali': 'sonalykumar17@gmail.com'
}


# Speak Function
def talk(text):
    print(f"🤖 Assistant: {text}")  # Print spoken text
    engine.say(text)
    engine.runAndWait()


# Get voice input
def get_info():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration=1)  # Reduce noise
            print("🎤 Listening...")
            voice = listener.listen(source, timeout=5)  # 5 sec timeout
            info = listener.recognize_google(voice)
            print(f"👤 You said: {info}")  # Print user's speech
            return info.lower()
    except sr.UnknownValueError:
        talk("Sorry, I couldn't understand. Please repeat.")
        return None
    except sr.RequestError:
        talk("Network error. Please check your connection.")
        return None
    except Exception as e:
        print(e)
        return None


# Send Email
def send_email(receiver, subject, message):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        email_message = EmailMessage()
        email_message['From'] = sender_email
        email_message['To'] = receiver
        email_message['Subject'] = subject
        email_message.set_content(message)
        server.send_message(email_message)
        server.quit()
        talk("✅ Your email has been sent.")
    except Exception as e:
        talk("❌ Error sending the email.")
        print(e)


# Read Emails
def read_emails():
    global current_index, email_ids
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(sender_email, sender_password)
        mail.select("inbox")

        if not email_ids:  # Fetch emails only once
            status, messages = mail.search(None, "ALL")
            if status != "OK" or not messages[0]:
                talk("No emails found in your inbox.")
                return
            email_ids.extend(messages[0].split())
            current_index = len(email_ids) - 1  # Start with the latest email

        while True:
            try:
                email_id = email_ids[current_index]
                status, msg_data = mail.fetch(email_id, "(RFC822)")
                if status == "OK":
                    for response_part in msg_data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_bytes(response_part[1])
                            subject, encoding = decode_header(msg["Subject"])[0]
                            if isinstance(subject, bytes):
                                subject = subject.decode(encoding if encoding else "utf-8")
                            from_ = msg.get("From")
                            talk(f"Email from {from_}, subject: {subject}")
            except Exception as e:
                talk("❌ Error reading email. Say 'next', 'previous', 'once again', or 'exit'.")
                print(e)
                continue

            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                talk(
                    "Say 'next' for the next email, 'previous' for the previous email, 'once again' to repeat, or 'exit' to stop.")
                recognizer.adjust_for_ambient_noise(source)
                try:
                    print("listiening....")
                    audio = recognizer.listen(source,timeout=10)
                    user_input = recognizer.recognize_google(audio).lower()
                    print("you said:",user_input)
                except sr.UnknownValueError:
                    talk("Sorry, I didn't catch that. Please try again.")
                    continue
                except sr.RequestError:
                    talk("Speech recognition service is unavailable.")
                    continue

            if "next" in user_input:
                if current_index > 0:
                    current_index -= 1
                else:
                    talk("This is the latest email.")
            elif "previous" in user_input:
                if current_index < len(email_ids) - 1:
                    current_index += 1
                else:
                    talk("This is the oldest email.")
            elif "once again" in user_input:
                continue  # Repeat the same email
            elif "exit" in user_input:
                break
            else:
                talk("Invalid input. Please say 'next', 'previous', 'once again', or 'exit'.")

        mail.logout()
    except Exception as e:
        talk("❌ Error accessing emails. Please try again later.")
        print(e)


email_ids = []
current_index = -1


# Delete Email
def delete_email():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(sender_email, sender_password)
        mail.select("inbox")

        status, messages = mail.search(None, "ALL")
        if status != "OK" or not messages[0]:
            talk("No emails found in your inbox.")
            return

        latest_email_id = messages[0].split()[-1]
        talk("Do you want to delete the latest email? Say 'ok' to confirm.")
        confirmation = get_info()

        if confirmation and "ok" in confirmation:
            mail.store(latest_email_id, "+FLAGS", "\\Deleted")
            mail.expunge()
            talk("✅ The email has been deleted.")
        else:
            talk("❌ Email deletion canceled.")

        mail.logout()
    except Exception as e:
        talk("❌ Error deleting email.")
        print(e)


# Check Email Contact
def check_word_in_email_list(text):
    words = text.lower().split()
    for word in words:
        if word in email_list:
            talk(f"{word} is found in email list.")
            return word
    talk("No match found in email list.")
    return None


# Send Email Action
def send_email_action():
    while True:
        talk('To whom would you like to send the email?')
        name = get_info()
        if name == "close":
            talk("Exiting email assistant.")
            return

        contact_name = check_word_in_email_list(name)
        if not contact_name:
            talk("Sorry, I couldn't find that contact.")
            continue

        receiver = email_list.get(contact_name)
        talk('What is the subject of your email?')
        subject = get_info()
        if subject == "close":
            talk("Exiting email assistant.")
            return

        talk('Tell me the text in your email.')
        message = get_info()
        if message == "close":
            talk("Exiting email assistant.")
            return

        send_email(receiver, subject, message)
        talk("Do you want to send another email?")
        response = get_info()
        if response == "close" or "no" in response:
            talk("Exiting email assistant.")
            return


# Get User Action
def get_email_info():
    while True:
        talk('What would you like to do? Send, read, or delete an email?')
        action = get_info()
        if action == "close":
            talk("Exiting email assistant.")
            return

        if action:
            if 'send' in action:
                send_email_action()
            elif 'read' in action:
                read_emails()
            elif 'delete' in action:
                delete_email()
            else:
                talk("Sorry, I didn't understand. Say 'send', 'read', or 'delete'.")

        talk("Do you want to perform another email action?")
        response = get_info()
        if response == "close" or "no" in response:
            talk("Exiting email assistant.")
            return


# Start the email assistant
get_email_info()


