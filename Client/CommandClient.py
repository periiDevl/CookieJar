import socket
import subprocess
import threading

def RunClient(ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (ip, 12345)

    client_socket.connect(server_address)

    def receive_responses():
        while True:
            response = client_socket.recv(1024).decode()
            print("Server Response:")
            print(response)

    response_thread = threading.Thread(target=receive_responses)
    response_thread.start()

    try:
        while True:
            command = input("Enter a command to send to the server (or 'exit' to quit): ")

            if command.lower() == 'exit':
                client_socket.send(("command:exit").encode())  # Send an exit command to the server
                break

            if command.strip():
                client_socket.send(("command:" + command).encode())

    except Exception as e:
        print(f"Error: {e}")

    client_socket.close()
