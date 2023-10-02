import socket
from tkinter import *
from PIL import Image, ImageTk
import io
import subprocess
import threading
import queue
import time
import warnings
import CommandClient
warnings.filterwarnings("ignore", category=DeprecationWarning)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = input("Enter an ip adress : ")

server_address = (ip, 12345)

client_socket.connect(server_address)

desired_resolution = (854, 480) 

root = Tk()
root.title("Received Image Data From " + ip)

image_label = Label(root)
image_label.pack()

image_queue = queue.Queue()

command_queue = queue.Queue()

def receive_and_display_image():
    try:
        while True:
            img_size_bytes = client_socket.recv(4)
            if not img_size_bytes:
                break
            img_size = int.from_bytes(img_size_bytes, byteorder='big')

            img_data = b''
            while len(img_data) < img_size:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break 
                img_data += chunk

            image = Image.open(io.BytesIO(img_data))

            image = image.resize(desired_resolution, Image.ANTIALIAS)

            image = ImageTk.PhotoImage(image)

            image_queue.put(image)

    except Exception as e:
        print(f"Error: {e}")


def request_screenshots():
    try:
        while True:
            client_socket.send("screenshot".encode())
            time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")


image_thread = threading.Thread(target=receive_and_display_image)
image_thread.daemon = True
image_thread.start()

screenshot_thread = threading.Thread(target=request_screenshots)
screenshot_thread.daemon = True
screenshot_thread.start()

def update_image_label():
    try:
        while True:
            
            image = image_queue.get()
            image_label.config(image=image)
            image_label.image = image
            root.update()

    except Exception as e:
        print(f"Error: {e}")

update_image_label_thread = threading.Thread(target=update_image_label)
update_image_label_thread.daemon = True
update_image_label_thread.start()
def runCommandClient():
    CommandClient.RunClient(ip)
CommandClient_thread = threading.Thread(target=runCommandClient)
CommandClient_thread.daemon = True
CommandClient_thread.start()

root.mainloop()
