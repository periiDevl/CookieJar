import socket
def RunClient(ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (ip, 12345) 

    client_socket.connect(server_address)

    try:
        while True:
            
            command = input("Enter a command to send to the server (or 'exit' to quit): ")

            if command.lower() == 'exit':
                break

            if command.strip():
                
                client_socket.send(("command:" + command).encode())

                
                response = client_socket.recv(1024).decode()
                print("Server Response:")
                print(response)

    except Exception as e:
        print(f"Error: {e}")

    
    client_socket.close()
