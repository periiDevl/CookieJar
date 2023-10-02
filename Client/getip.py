import socket

# Get the hostname of the local machine
hostname = socket.gethostname()

# Get the IP address corresponding to the hostname
ip_address = socket.gethostbyname(hostname)

print(f"Server IP address: {ip_address}")
