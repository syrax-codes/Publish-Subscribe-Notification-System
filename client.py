import socket
import threading
import ssl

HOST = '172.20.10.2'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

context = ssl._create_unverified_context()
secure_client = context.wrap_socket(client, server_hostname="localhost")

secure_client.connect((HOST, PORT))


def receive():
    while True:
        try:
            data = secure_client.recv(1024)
            if not data:
                break
            print(data.decode(), end="")
        except:
            break


# Start receiving thread
threading.Thread(target=receive, daemon=True).start()


#  LOGIN PROCESS
username = input("Enter Username: ")
secure_client.send((username + "\n").encode())

password = input("Enter Password: ")
secure_client.send((password + "\n").encode())


# Normal messaging
while True:
    msg = input()
    secure_client.send(msg.encode())
