import socket

def connect_to_remote_server(hostname, port):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((hostname, port))
        print(f"Connected to {hostname} on port {port}")

        # Send data to the server
        message = "Hello, server!"
        client_socket.sendall(message.encode())

        # Receive data from the server
        data = client_socket.recv(1024)
        print("Received:", data.decode())

    except ConnectionRefusedError:
        print("Connection refused. Make sure the server is running and the correct port is specified.")
    finally:
        # Close the socket
        client_socket.close()

# Example usage
remote_hostname = "192.168.10.32"  # Replace with the remote server's hostname or IP address
remote_port = 3001  # Replace with the port the server is listening on
connect_to_remote_server(remote_hostname, remote_port)

