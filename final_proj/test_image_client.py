import socket

def send_image(image_path, host, port):
    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the server
        s.connect((host, port))
        
        # Open the image file
        with open(image_path, 'rb') as f:
            # Read and send image data in chunks
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                s.sendall(chunk)

    print("Image sent successfully")

# Example usage
image_path = "yuju.jpg"
host = "localhost"
port = 12345
send_image(image_path, host, port)
