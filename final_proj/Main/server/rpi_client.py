import socket
import pyaudio
import time
import threading
import subprocess

# Main server address and port
MAIN_SERVER_IP = 'devin-ASUS-TUF-Gaming-A15-FA507XI-FA507XI.local'  # Change this to your server IP address
MAIN_SERVER_PORT = 6000       # Change this to your server port number

# STM32 server port
STM32_PORT = 12345

STOP_SIGNAL = b"__STOP__"
NAME = "yuju"

def vote(client_socket, value):
    """
    Send a voting request to the server using the same socket.
    """
    try:
        message = f"vote {NAME} {value}"
        client_socket.sendall(message.encode())
        print("Voting request sent!")

        response = client_socket.recv(1024)
        print("Response from server:", response.decode())

    except Exception as e:
        print("An error occurred while sending voting request:", e)

def take_picture():
    try:
        # Execute the libcamera-still command to take a picture
        subprocess.run(["libcamera-still", "-e", "png", "-o", f"{NAME}.png"], check=True)
        print(f"Picture taken and saved as {NAME}.png")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while taking the picture: {e}")

def signin(client_socket):
    """
    Send a message and an image to the server using the same socket.
    """
    take_picture()
    message = f"signin {NAME}"
    image_path = f"{NAME}.jpg"
    try:
        # Send the message
        client_socket.sendall(message.encode())
        print("Message sent:", message)

        # Wait for response
        response = client_socket.recv(1024)
        print("Response from server:", response.decode())

        # Open the image file
        with open(image_path, 'rb') as f:
            # Read and send image data in chunks
            while chunk := f.read(1024):
                client_socket.sendall(chunk)
        client_socket.sendall(STOP_SIGNAL)
        print("Image sent! Waiting for verification...")

        # Wait for final response
        response = client_socket.recv(1024)
        print("Response from server:", response.decode())

    except Exception as e:
        print("An error occurred while sending message and image:", e)

def speak(client_socket):
    """
    Send audio data to the server using the same socket.
    """
    CHUNK = 128
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    try:
        client_socket.sendall(f"speaking {NAME}".encode())
        response = client_socket.recv(1024)
        print("Response from server:", response.decode())
        if response == b"Start speaking":
            duration = float(client_socket.recv(1024).decode())
            print(f"Start speaking for {duration} seconds...")
            start_time = time.time()
            while time.time() - start_time <= duration:
                data = stream.read(CHUNK)
                client_socket.sendall(data)
            client_socket.sendall(STOP_SIGNAL)
        else:
            print("You are not allowed to speak")

    except Exception as e:
        print("An error occurred while sending audio:", e)
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

def main():
    global stored_vote_value
    stored_vote_value = None
    signed = False

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (MAIN_SERVER_IP, MAIN_SERVER_PORT)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)
    print(f"Connected to {server_address}")
    stm32_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    stm32_server_socket.bind(('0.0.0.0', STM32_PORT))
    stm32_server_socket.listen()
    print(f"STM32 server listening on port {STM32_PORT}")
    # vote(client_socket, "yes")

    try:
        while True:
            stm32_socket, addr = stm32_server_socket.accept()
            print(f"Connection from STM32 at {addr}")
            while True:
                message = stm32_socket.recv(1024).decode()
                if message == "2":
                    if not signed:
                        signin(client_socket)
                        signed = True
                    else:
                        speak(client_socket)
                elif message == "1":
                    vote(client_socket, "no")
                elif message == "0":
                    vote(client_socket, "yes")
                else:
                    print("Invalid message received from STM32:", message)
                    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        stm32_server_socket.close()
        client_socket.close()
        print("Connections closed")


if __name__ == "__main__":
    vote_lock = threading.Lock()
    main()
