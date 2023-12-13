import socket
import threading
from terminal import success, error

clients = {}
lock = threading.Lock()

def broadcast(message, sender_username):
    with lock:
        for client_socket, username in clients.items():
            if username != sender_username:
                try:
                    client_socket.send(f"{sender_username}: {message}".encode('utf-8'))
                except:
                    error(f"Error broadcasting message to {username}")

def handle_client(client_socket, username):
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"{username} has disconnected.")
                with lock:
                    del clients[client_socket]
                break
            success(f"{username}: {message}")
            broadcast(message, username)
    except:
        error(f"{username} has encountered an error. Disconnecting...")
        with lock:
            del clients[client_socket]

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12346))
    server.listen(5)
    success("Server listening on port 12345")

    while True:
        client_socket, addr = server.accept()
        username = client_socket.recv(1024).decode('utf-8')
        success(f"New connection from {addr}, username: {username}")

        client_socket.send("You are now connected to the chatroom.".encode('utf-8'))

        with lock:
            clients[client_socket] = username

        threading.Thread(target=handle_client, args=(client_socket, username)).start()

if __name__ == "__main__":
    main()
