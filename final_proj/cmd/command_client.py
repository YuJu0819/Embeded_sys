import socket
import sys

def send_message(port, message):
    server_address = ('localhost', port)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(server_address)
            sock.sendall(message.encode())
            response = sock.recv(1024)
    except ConnectionRefusedError:
        print("Connection refused. Ensure the server is running and the port is correct.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    
    port = 5000
    send_message(port, "Hello, server!")
