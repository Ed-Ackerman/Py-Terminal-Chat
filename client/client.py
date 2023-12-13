import socket
import threading
from terminal import info, success, error, input_prompt
from rich import print
import msvcrt
import keyboard

print_lock = threading.Lock()

def receive_messages(client_socket, username):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print_message(message, username)
        except:
            error("Error receiving messages.")
            break

def print_message(message, username):
    with print_lock:
        if message.startswith(username + ":"):
            success(f"{' ' * 50}{message[len(username) + 1:]}")
        else:
            info(f"{message}")
def handle_user_input(client_socket):
    input_text = ""
    first_character_entered = False
    enter_pressed = False

    while True:
        if msvcrt.kbhit():
            char = msvcrt.getch()
            if char == b'\r':  # Enter key
                enter_pressed = True
            elif char.decode('utf-8', errors='ignore').isprintable() or char in (b'\b', b'\x7f'):  # Check if printable, backspace, or delete
                if char.isalnum() or char.isspace() or char in b"!@#$%^&*()-_=+[]{}|;:'\",.<>/?":
                    input_text += char.decode('utf-8', errors='ignore')

                if not first_character_entered:
                    print("[bold cyan]  You:[/bold cyan]", end='', flush=True)
                    first_character_entered = True

                if char in (b'\b', b'\x7f', b'S' , b'\x08'):  # Backspace or Delete key
                    if input_text:
                        input_text = input_text[:-1]  # Remove last character
                        msvcrt.putch(b'\b')  # Move the cursor back
                        msvcrt.putch(b' ')   # Print a space to erase the character
                        msvcrt.putch(b'\b')  # Move the cursor back again
                else:
                    print(char.decode('utf-8', errors='ignore'), end='', flush=True)

            elif char == b'\x03':  # Ctrl+C
                break

        # Check if Enter was pressed and send the message
        if enter_pressed:
            message = input_text.strip()
            if message:
                print("\n", end='', flush=True)
                client_socket.send(message.encode('utf-8'))
                input_text = ""
                first_character_entered = False
                enter_pressed = False
        
        # Check for arrow key presses
        if keyboard.is_pressed('left'):
            # Handle left arrow key
            pass
        elif keyboard.is_pressed('right'):
            # Handle right arrow key
            pass
        elif keyboard.is_pressed('up'):
            # Handle up arrow key
            pass
        elif keyboard.is_pressed('down'):
            # Handle down arrow key
            pass

def main():
    username = input_prompt("Enter your username: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 12346))

    # Send username as bytes
    client.send(username.encode('utf-8'))

    initial_message = client.recv(1024).decode('utf-8')
    success(initial_message)

    receive_thread = threading.Thread(target=receive_messages, args=(client, username))
    receive_thread.start()

    handle_user_input(client)

    # Clean up keyboard listener before exiting the thread
    keyboard.unhook_all()

if __name__ == "__main__":
    main()
