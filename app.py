import firebase_admin
from firebase_admin import credentials, firestore, messaging
from datetime import datetime
from cryptography.fernet import Fernet
import curses
import requests

current_user = ""

# Initialize Firebase
cred = credentials.Certificate('SCLIservicekey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()



# ENCRYPTION FUNCTIONS


def generate_key():
    return Fernet.generate_key()

# Encrypt the message using the encryption key
def encrypt(key, message):
    f = Fernet(key)
    return f.encrypt(message.encode()).decode()

# Decrypt the message using the encryption key
def decrypt_message(key, encrypted_message):
    f = Fernet(key)
    return f.decrypt(encrypted_message.encode()).decode()



# USER FUNCTIONS


# load_user function to load the encryption key of the user from the database
def load_user(username,password):
    user_ref = db.collection('users').document(username)
    doc = user_ref.get()
    if doc.exists:
        return doc.to_dict()['encryption_key'].encode()
    else:
        key = generate_key()
        user_ref.set({'username': username, 'online': True, 'last_seen': datetime.now(), 'encryption_key': key.decode(), 'password': encrypt(key, password)})
        return key

# Register a new user
def login_user(username,password):
    user_ref = db.collection('users').document(username)
    password = encrypt(load_user(username,password),password)
    doc = user_ref.get()
    if doc.exists:
        user_data = doc.to_dict()
        stored_password = user_data['password']
        if password == stored_password:
            user_ref.update({'online': True, 'last_seen': datetime.now()})
            return username, user_data['encryption_key'].encode()
        else:
            print("Invalid password")
            return 1,1
    else:
        print("User does not exist")
        return None, None

# Logout the user
def logout_user(username):
    user_ref = db.collection('users').document(username)
    user_ref.update({'online': False, 'last_seen': datetime.now()})



# CHAT FUNCTIONS


# Function to get the list of online users
def get_online_users():
    users_ref = db.collection('users').where('online', '==', True)
    docs = users_ref.stream()
    return [doc.id for doc in docs]

# Function to send a message
def send_message(sender, receiver, key, message):
    encrypted_message = encrypt(key, message)
    db.collection('messages').add({
        'sender': sender,
        'receiver': receiver,
        'message': encrypted_message,
        'timestamp': datetime.now()
    })
    send_push_notification(receiver, message)

# Function to get all messages between two users
def get_all_messages(user1, user2, key):
    messages_ref = db.collection('messages') \
                     .where('sender', 'in', [user1, user2]) \
                     .where('receiver', 'in', [user1, user2]) \
                     .order_by('timestamp', direction=firestore.Query.DESCENDING)
    docs = messages_ref.stream()
    messages = []
    for doc in docs:
        data = doc.to_dict()
        decrypted_message = decrypt_message(key, data['message'])
        data['message'] = decrypted_message
        messages.append(data)
    return messages

# Function to send a push notification
def send_push_notification(receiver, message):
    user_ref = db.collection('users').document(receiver)
    user = user_ref.get().to_dict()
    if 'fcm_token' in user:
        fcm_token = user['fcm_token']
        message = messaging.Message(
            notification=messaging.Notification(
                title='New Message',
                body=message,
            ),
            token=fcm_token,
        )
        response = messaging.send(message)
        print('Successfully sent message:', response)



# MENU FUNCTIONS


# Path: chat.py (curses-based chat application)
def draw_menu(stdscr, current_user):
    global current_username
    current_username = current_user
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, f"Logged in as: {current_user}")
    stdscr.addstr(2, 0, "Online Users:")

    online_users = get_online_users()
    for idx, user in enumerate(online_users):
        stdscr.addstr(4 + idx, 0, f"{idx + 1}. {user}")
    
    stdscr.addstr(len(online_users) + 6, 0, "Select user to chat: (Enter number)")
    stdscr.refresh()

# Function to draw the chat interface
def draw_chat(stdscr, current_user, chat_user, key):
    stdscr.clear()
    stdscr.addstr(0, 0, f"Chatting with: {chat_user}")
    stdscr.addstr(1, 0, "Type your message and press Enter (type 'exit' to exit):")
    stdscr.refresh()
    curses.echo()

    while True:
        stdscr.move(2, 0)
        message = stdscr.getstr().decode("utf-8")
        if message.lower() == 'exit':
            break
        send_message(current_user, chat_user, key, message)
        draw_message_history(stdscr, current_user, chat_user, key)

    # Return to the main menu after exiting chat
    draw_menu(stdscr, current_user)

# Function to draw the message history
def draw_message_history(stdscr, user1, user2, key):
    stdscr.clear()
    stdscr.addstr(0, 0, f"Chatting with: {user2}")
    stdscr.addstr(1, 0, "Chat Box :")
    messages = get_all_messages(user1, user2, key)
    for idx, msg in enumerate(reversed(messages)):
        stdscr.addstr(3 + idx, 0, f"{msg['timestamp']} - {msg['sender']}: {msg['message']}")
    stdscr.refresh()    
    stdscr.addstr(len(messages) + 5, 0, "Type your message and press Enter:")
    stdscr.refresh()

# Main function to run the chat application
def main(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Enter your username: ")
    stdscr.refresh()
    curses.echo()
    username = stdscr.getstr().decode("utf-8")
    stdscr.clear()
    stdscr.addstr(0, 0, "Enter your password: ")
    stdscr.refresh()
    curses.noecho()
    password = stdscr.getstr().decode("utf-8")
    curses.echo()
    current_user, key = login_user(username, password)
    if current_user is None:
        stdscr.clear()
        stdscr.addstr(0, 0, "User does not exist. Creating new user...")
        stdscr.refresh()
        key = load_user(username,password)
        current_user = username
    else:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Try again Later{current_user}")
        stdscr.refresh()
        return None

    while True:
        draw_menu(stdscr, current_user)
        choice = int(stdscr.getstr(len(get_online_users()) + 8, 0).decode("utf-8")) - 1
        chat_user = get_online_users()[choice]
        draw_chat(stdscr, current_user, chat_user, key)

# Run the chat application
if __name__ == "__main__":
    import os
    if os.name == 'nt':
        import sys
        import msvcrt
        import _curses

        if not hasattr(msvcrt, 'getch'):
            raise ImportError('msvcrt.getch not found, cannot run on this system')

        # Define a replacement for the missing curses functions on Windows
        def _curses_noop(*args, **kwargs):
            pass

        for attr in dir(_curses):
            if attr.startswith('mouse'):
                setattr(_curses, attr, _curses_noop)

    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        logout_user(current_user)
        curses.endwin()
        print("Chat application closed")