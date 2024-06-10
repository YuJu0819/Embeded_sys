import socket
import threading
import time
import csv
import cv2
import numpy as np
import pyaudio
from utils import initialize_csv, attendant_signin, attendant_vote, verify
# Global state
current_mode = "general"
current_issue = ""
is_voting = False
allowed_speaking = False
lock = threading.Lock()

STOP_SIGNAL = b"__STOP__"

# Audio Configuration
CHUNK = 128
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
 
speaking_duration = 0

# CSV file setup
attendant_file = "attendants.txt"
csv_file = "meeting_database.csv"

def recv_image(client_socket):
    # Receive image data in chunks
    image_data = b''
    while True:
        chunk = client_socket.recv(1024)
        if STOP_SIGNAL in chunk:
            chunk = chunk.replace(STOP_SIGNAL, b'')
            image_data += chunk
            break
        image_data += chunk

    # Decode the image data to a numpy array
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    print("Image received successfully")
    return img 

def start_speaking(client_socket, name):
    global speaking_duration, is_speaking
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)
    try:
        client_socket.sendall(f"{speaking_duration}".encode())
        while True:
            data = client_socket.recv(1024)
            if not data or data == STOP_SIGNAL:
                break
            stream.write(data)
            
    except ConnectionResetError:
        print("Connection with client was reset")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        is_speaking = False
        print(f"{name} stopped speaking")


def start_voting(issue, duration=10):
    global current_issue, current_state, is_voting
    current_issue = issue
    current_state = "voting"
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
    rows[0].append(current_issue)
    for row in rows[1:]:
        row.append(" ")
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    print(f"Voting started for issue '{current_issue}' for {duration} seconds")
    is_voting = True
    time.sleep(duration)
    is_voting = False
    print(f"Voting ended for issue '{current_issue}'")

# Functions to handle client connections
def handle_command_client(client_socket, address):
    global current_mode, speaking_duration, allowed_speaking
    print(f"Command connection established with {address}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            if is_voting:
                client_socket.sendall(b"Voting in progress, please wait")
                break
            command = data.decode()
            command = command.split(" ")
            print(f"Received command: {command}")
            if current_mode == "general":
                if command[0] == "start": # receive command to start meeting
                    current_mode = "meeting"
                    notification = "Meeting started"
                    print(f"{notification}, Mode changed to '{current_mode}'")
                    client_socket.sendall(notification.encode())

                else:
                    client_socket.sendall(b"Invalid command")
                    continue

            elif current_mode == "meeting":
                if command[0] == "end":
                    current_mode = "general"
                    notification = "Meeting ended"
                    print(f"{notification}, Mode changed to '{current_mode}'")  
                    client_socket.sendall(notification.encode())

                elif command[0] == "voting":
                    issue = command[1]
                    duration = int(command[2]) if len(command) > 2 else 10
                    client_socket.sendall(f"Voting started for issue '{issue}'... ends in {duration} secconds".encode())
                    threading.Thread(target=start_voting, args=(issue, duration)).start()

                elif command[0] == "speaking":
                    allowed_speaking = True
                    speaking_duration = float(command[1]) if len(command) > 1 else 10
                    client_socket.sendall(f"Allow speaking".encode())
                else:
                    client_socket.sendall(b"Invalid command")
                    continue
            else:   
                client_socket.sendall(b"Something went wrong...")
                continue
    except ConnectionResetError:
        print(f"Command connection with {address} was reset")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        print(f"Command connection with {address} closed")

def handle_rpi_client(client_socket, address):
    global current_mode, allowed_speaking, is_voting
    print(f"Info connection established with {address}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode()
            message = message.split(" ")
            print(f"Received message: {message}")

            ### Handle request received before meeting starts
            if current_mode == "general": 
                if message[0] == "signin": # receive request to sign in
                    name = message[1]
                    client_socket.sendall(f"Please send {name}'s image for verification".encode())
                    image = recv_image(client_socket)
                    if verify(name, image): # verify the image and sign in for the attendant
                        print(f"Attendant '{name}' signed in!")
                        attendant_signin(name, csv_file) 
                        client_socket.sendall(b"Signin successful")
                    else:
                        client_socket.sendall(b"Signin failed")
                else:
                    client_socket.sendall(b"Invalid command")
            
            ### Handle request received during meeting
            elif current_mode == "meeting":
                if message[0] == "speaking" and not is_voting: # receive request to start speaking
                    name = message[1]
                    if allowed_speaking: # check if speaking is allowed
                        client_socket.sendall(b"Start speaking")
                        start_speaking(client_socket, name)
                    else:
                        client_socket.sendall(f"Wait for discussion".encode())

                elif message[0] == "vote" and is_voting: # receive request to vote
                    name = message[1]
                    value = message[2]
                    attendant_vote(name, value, csv_file, current_issue)
                    client_socket.sendall(b"Vote received")
                    pass

                elif message[0] == "signin": # handle late sign in
                    name = message[1]
                    client_socket.sendall(f"Please send {name}'s image for verification".encode())
                    image = recv_image(client_socket)
                    if verify(name, image):
                        print(f"Attendant '{name}' signed in!")
                        attendant_signin(name, csv_file, late=True)
                        client_socket.sendall(b"Signin successful")
                    else:
                        client_socket.sendall(b"Signin failed")
                else:
                    client_socket.sendall(b"Invalid command")
            else:
                client_socket.sendall(b"Something went wrong...")
    except ConnectionResetError:
        print(f"Info connection with {address} was reset")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        print(f"Info connection with {address} closed")

def start_server(port, handler):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")
    while True:
        try:
            client_socket, address = server_socket.accept()
            client_handler = threading.Thread(target=handler, args=(client_socket, address))
            client_handler.start()
        except socket.error:
            break
    server_socket.close()

if __name__ == "__main__":

    # Load attendants list and initialize CSV file
    initialize_csv(attendant_file, csv_file)

    # Define ports
    command_port = 5000
    rpi_port = 6000

    # Create and start threads for each port
    command_thread = threading.Thread(target=start_server, args=(command_port, handle_command_client))
    rpi_thread = threading.Thread(target=start_server, args=(rpi_port, handle_rpi_client))

    command_thread.start()
    rpi_thread.start()

    command_thread.join()
    rpi_thread.join()

