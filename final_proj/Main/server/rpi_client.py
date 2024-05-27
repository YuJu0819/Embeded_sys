import socket
import sys

def send_message(port, message):
    server_address = ('localhost', port)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(server_address)
            print(f"Connected to {server_address}")
            sock.sendall(message.encode())
            response = sock.recv(1024)
            print(f"Received response: {response.decode()}")
    except ConnectionRefusedError:
        print("Connection refused. Ensure the server is running and the port is correct.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sender.py <port>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    message_face = "face verified"
    message_vote = "vote"
    name = "Bob"
    issue = "issue1"
    message = f"{message_vote}, {name}, yes"
    
    
    send_message(port, message)
