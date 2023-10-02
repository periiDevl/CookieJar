import socket
from PIL import ImageGrab, ImageDraw, Image
import time
import io
import subprocess
import threading
import pyautogui
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('0.0.0.0', 12345) 
server_socket.bind(server_address)

server_socket.listen(1)

print("Server is listening for incoming connections...")

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break 
            
            if data.startswith("command:"):
                command = data[len("command:"):]
                
                output = subprocess.getoutput(command)
                client_socket.send(output.encode())
            elif data == "screenshot":
                screenshot = ImageGrab.grab()
                draw = ImageDraw.Draw(screenshot)

                mouse_x, mouse_y = pyautogui.position()

                circle_radius = 10
                outline_width = 4
                outline_color = "red"
                draw.ellipse((mouse_x - circle_radius, mouse_y - circle_radius,
                              mouse_x + circle_radius, mouse_y + circle_radius),
                             outline=outline_color, width=outline_width)

                img_byte_array = io.BytesIO()
                screenshot.save(img_byte_array, format="JPEG")
                img_bytes = img_byte_array.getvalue()
                img_byte_array.close()

                img_size = len(img_bytes)
                client_socket.sendall(img_size.to_bytes(4, byteorder='big'))

                for i in range(0, len(img_bytes), 1024):
                    chunk = img_bytes[i:i+1024]
                    client_socket.sendall(chunk)
                print("Screenshot sent successfully.")
                time.sleep(0.5)
        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
