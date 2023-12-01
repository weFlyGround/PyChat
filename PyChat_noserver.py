#stable 1.7
from colorama import Fore, Style

version = "1.7"
print(f"{Fore.GREEN}Version:{Style.RESET_ALL}", version)

import os
import pyrebase
import re
import time
from datetime import datetime

config = {
  #"apiKey": 
  #"authDomain": 
  #"databaseURL": 
  #"storageBucket": 
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def is_valid_username(username):
    pattern = re.compile(r'^[a-zA-Z0-9_]+$')
    return bool(pattern.match(username))

def read_username():
    try:
        with open("username.txt", "r") as file:
            username = file.read().strip()
            while not is_valid_username(username):
                print("Invalid username format.")
                username = input("Enter a valid username (only letters, digits, and underscores allowed): ")
            return username
    except FileNotFoundError:
        print("username.txt file not found.\nIt will be saved when you choose your username")
        username = input("\nEnter your name: ")
        while not is_valid_username(username):
            print("Invalid username format.")
            username = input("Enter a valid username (only letters, digits, and underscores allowed): ")
        with open("username.txt", "w") as file:
            file.write(username)
        return username

def send_message():
    username = read_username()

    message = input("Enter your message: ")

    data = {
        "sender": username,
        "message": message,
        "timestamp": str(datetime.now())  # Add the current timestamp to the message data
    }
    db.child("messages").push(data)
    print("\nMessage sent!")
    time.sleep(1)

def highlight_mentions(text, current_username):
    # Regular expression to find mentions (words starting with @)
    pattern = re.compile(r'@\w+')
    highlighted_text = text
    for mention in pattern.findall(text):
        username = mention[1:]
        if username == current_username:
            # Highlight mentions with bright green color if it matches the current user's username
            highlighted_text = highlighted_text.replace(mention, f"{Fore.GREEN}{mention}{Style.RESET_ALL}")
    return highlighted_text

def read_messages():
    current_username = read_username()
    if current_username == "":
        # Return an empty string if the current_username is empty (None was replaced by an empty string)
        return ""

    messages = db.child("messages").get()

    if messages.each():
        for message in messages.each():
            message_data = message.val()
            sender = message_data.get("sender")
            message_text = message_data.get("message")
            timestamp = message_data.get("timestamp")
            timestamp_datetime = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
            timestamp_str = timestamp_datetime.strftime("[%d-%m-%Y; %H:%M]")

            if sender == current_username:
                print(f"{Fore.CYAN}You{Style.RESET_ALL} {timestamp_str}: {highlight_mentions(message_text, current_username)}")
            else:
                print(f"{Fore.YELLOW}{sender}{Style.RESET_ALL} {timestamp_str}: {highlight_mentions(message_text, current_username)}")
    else:
        print("No messages found.")

def clear_messages():
    db.child("messages").remove()
    print("All messages have been cleared.")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        print("\nChoose an action:")
        print("1. Send a message")
        print("2. Read messages")
        print("3. Exit")
        print("4. Clear all messages (admin function)")
        print("5. View credits")
        print(f"{Fore.CYAN}clear{Style.RESET_ALL}. to clear the console")

        choice = input("\nYour choice: ")

        if choice == "1":
            os.system('cls' if os.name == 'nt' else 'clear')
            send_message()
        elif choice == "2":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(" ")
            print("-" * 100)
            read_messages()
            print("-" * 100)
        elif choice == "3":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\nExiting the application.")
            time.sleep(1)
            break
        elif choice == "4":
            print(f"{Fore.RED}NOTICE!{Style.RESET_ALL} This function will clear {Fore.MAGENTA}ALL{Style.RESET_ALL} the messages on the server! (admin function)")
            clearchoose = input("Proceed? (Y or N): ")
            if clearchoose.lower() == "y":
                password = input("Password: ")
                if password == "password":
                    try:
                        clear_messages()
                        time.sleep(1)
                    except Exception:
                        print(f"{Fore.RED}ERROR SROWN! {Style.RESET_ALL}Access blocked! Reason: 404 Forbidden")
                else:
                    print("You are not admin! Get out of here!")
            elif clearchoose.lower() == "n":
                print("Clearing message data has been canceled.")
        elif choice == "5":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"\n{Fore.CYAN}Developer:{Style.RESET_ALL} PlazmaRoma, FlyGround team\nOur GitHub: https://github.com/weFlyGround\nYoutube(Gaming): https://www.youtube.com/channel/UCnE9fW8qdkyAtbThMvm4m3A [KZ]\n{Fore.MAGENTA}Special Thanks:{Style.RESET_ALL} Ilya Nurullaev (tester) [KZ], Standalone Coder (the mastermind) [RU], And thank YOU too! (user) [?]\n{Fore.GREEN}Version:{Style.RESET_ALL} {version}")
            with open("credits.txt", "w") as file:
                file.write("Developer: PlazmaRoma, FlyGround team\nOur GitHub: https://github.com/weFlyGround\nYoutube(Gaming): https://www.youtube.com/channel/UCnE9fW8qdkyAtbThMvm4m3A [KZ]\nSpecial Thanks: Ilya Nurullaev (tester) [KZ], Standalone Coder (the mastermind) [RU], And thank YOU too! (user) [?]\nVersion: 1.7")
            print("\nCredits have been added to credit.txt in the 'dist' folder")
        elif choice == "clear" or "Clear" or "CLEAR":
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
