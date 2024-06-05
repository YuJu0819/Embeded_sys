import socket

def receive_image(save_path, host, port):
    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind the socket to the address and port
        s.bind((host, port))
        # Listen for incoming connections
        s.listen()
        
        print("Waiting for a connection...")
        conn, addr = s.accept()
        
        with conn:
            print(f"Connected to {addr}")
            # Open a new file to save the received image
            with open(save_path, 'wb') as f:
                # Receive and write image data in chunks
                while True:
                    chunk = conn.recv(1024)
                    if not chunk:
                        break
                    f.write(chunk)

    print("Image received successfully")

# Example usage
save_path = "received_image.jpg"
host = "localhost"
port = 12345
receive_image(save_path, host, port)
