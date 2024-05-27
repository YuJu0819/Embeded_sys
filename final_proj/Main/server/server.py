import socket
import threading
import csv

# Global state
current_mode = "general"
current_issue = ""
lock = threading.Lock()

# CSV file setup
csv_file = "meeting_database.csv"
csv_lock = threading.Lock()

# Load attendants list
attendants = []

def initialize_attendants():
    global attendants
    try:
        with open("attendants.txt", "r") as file:
            attendants = [line.strip() for line in file.readlines()]
        print(f"Attendants loaded: {attendants}")
    except FileNotFoundError:
        print("Error: 'attendants.txt' file not found.")
        attendants = []

def initialize_csv():
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Attenandance"])
        for attendant in attendants:
            writer.writerow([attendant, "No"])
    print(f"CSV file {csv_file} initialized")

# Functions to update the CSV file
def update_attendance(name):
    global attendants
    with csv_lock:
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Attendance"])
            for row in rows[1:]:
                if row[0] == name:
                    row[1] = "Yes"
                writer.writerow(row)
    print(f"Attendance updated for {name}")

def new_issue(issue, default_value=""):
    global current_issue
    current_issue = issue
    with csv_lock:
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Add the new column to the header
        if current_issue not in rows[0]:
            rows[0].append(current_issue)

            # Add the default value for the new column to each row
            for row in rows[1:]:
                row.append(default_value)

            # Write the updated content back to the CSV file
            with open(csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            print(f"current_issue '{current_issue}' added to the CSV file")
        else:
            print(f"current_issue '{current_issue}' already exists in the CSV file")

def vote_for_issue(name, value):
    with csv_lock:
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Find the row corresponding to the name
        for row in rows[1:]:
            if row[0] == name:
                # Find the column corresponding to the issue
                for i, header in enumerate(rows[0]):
                    if header == current_issue:
                        # Update the value in the row
                        row[i] = value
                        break
                break

        # Write the updated content back to the CSV file
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        print(f"Issue '{current_issue}' updated for {name}")

# Functions to handle mode changes
def voting_end():
    global current_mode
    with lock:
        current_mode = "meeting"
    print(f"Voting ended. Mode changed to {current_mode}")

# Functions to handle client connections
def handle_command_client(client_socket, address):
    global current_mode
    print(f"Command connection established with {address}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            command = data.decode()
            print(f"Received command: {command}")
            mode = command.split(", ")[0]
            print(f"Mode: {mode}" )
            with lock:
                if mode == "general":
                    current_mode = "general"
                    print(f"Mode changed to {current_mode}")
                elif mode == "meeting":
                    current_mode = "meeting"
                    print(f"Mode changed to {current_mode}")
                elif mode == "voting":
                    current_mode = "voting"
                    print(f"Mode changed to {current_mode}")
                    issue = command.split(", ")[1]
                    new_issue(issue)
                    # Set a timer to end the voting
                    timer = threading.Timer(10, voting_end)
                    timer.start()
                else:
                    client_socket.sendall(b"Invalid command")
                    continue
            print(f"Mode changed to {current_mode} by {address}")
            client_socket.sendall(f"Mode changed to {current_mode}".encode())
    except ConnectionResetError:
        print(f"Command connection with {address} was reset")
    finally:
        client_socket.close()
        print(f"Command connection with {address} closed")

def handle_rpi_client(client_socket, address):
    global current_mode
    print(f"Info connection established with {address}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode()
            message = message.split(", ")
            match current_mode:
                case "general":
                    if message[0] == "face verified":
                        name = message[1]
                        update_attendance(name)
                case "meeting":
                    if message[0] == "mic on":
                        pass
                case "voting":
                    if message[0] == "vote":
                        name = message[1]
                        value = message[2]
                        vote_for_issue(name, value)
            with lock:
                mode = current_mode
            response = f"Received in {mode} mode: {message}"
            print(f"Received from {address} : {message}")
            client_socket.sendall(response.encode())
    except ConnectionResetError:
        print(f"Info connection with {address} was reset")
    finally:
        client_socket.close()
        print(f"Info connection with {address} closed")

def start_server(port, handler):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")
    while True:
        client_socket, address = server_socket.accept()
        client_handler = threading.Thread(target=handler, args=(client_socket, address))
        client_handler.start()

if __name__ == "__main__":

    # Load attendants list and initialize CSV file
    initialize_attendants()
    initialize_csv()

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

