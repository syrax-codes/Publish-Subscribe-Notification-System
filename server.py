import socket
import threading
import ssl

HOST = '0.0.0.0'
PORT = 5000

topics = {}
lock = threading.Lock()

# USER DATABASE
users = {
    "user1": {"password": "123", "premium": False},
    "user2": {"password": "123", "premium": True},
    "admin": {"password": "admin", "premium": True}
}

# Store authenticated clients
authenticated_clients = {}  # conn → username


def authenticate(conn):
    try:
        conn.send("Username: ".encode())
        username = conn.recv(1024).decode().strip()

        conn.send("Password: ".encode())
        password = conn.recv(1024).decode().strip()

        if username in users and users[username]["password"] == password:
            authenticated_clients[conn] = username
            conn.send("Authentication Successful\n".encode())
            return True
        else:
            conn.send("Authentication Failed\n".encode())
            return False
    except:
        return False


def process_command(conn, data):
    parts = data.split(" ", 2)
    command = parts[0]

    username = authenticated_clients.get(conn, None)

    if command == "SUBSCRIBE":
        if len(parts) < 2:
            conn.send("Invalid SUBSCRIBE\n".encode())
            return

        topic = parts[1]

        with lock:
            if topic not in topics:
                topics[topic] = []
            if conn not in topics[topic]:
                topics[topic].append(conn)

        conn.send(f"Subscribed to {topic}\n".encode())


    elif command == "UNSUBSCRIBE":
        if len(parts) < 2:
            conn.send("Invalid UNSUBSCRIBE\n".encode())
            return

        topic = parts[1]

        with lock:
            if topic in topics and conn in topics[topic]:
                topics[topic].remove(conn)

        conn.send(f"Unsubscribed from {topic}\n".encode())


    elif command == "PUBLISH":
        if len(parts) < 3:
            conn.send("Invalid PUBLISH\n".encode())
            return

        topic = parts[1]
        message = parts[2]

        with lock:
            if topic in topics:
                for subscriber in topics[topic][:]:
                    try:
                        subscriber.send(f"[{topic}] {message}\n".encode())
                    except:
                        topics[topic].remove(subscriber)


    # PREMIUM PUBLISH (NEW FEATURE)
    elif command == "PUBLISH_PREMIUM":
        if len(parts) < 3:
            conn.send("Invalid PUBLISH_PREMIUM\n".encode())
            return

        topic = parts[1]
        message = parts[2]

        with lock:
            if topic in topics:
                for subscriber in topics[topic][:]:
                    user = authenticated_clients.get(subscriber, None)

                    # Send only to premium users
                    if user and users[user]["premium"]:
                        try:
                            subscriber.send(f"[PREMIUM {topic}] {message}\n".encode())
                        except:
                            topics[topic].remove(subscriber)


    else:
        conn.send("Unknown command\n".encode())


def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")

    # AUTHENTICATION STEP
    if not authenticate(conn):
        conn.close()
        print(f"[AUTH FAILED] {addr}")
        return

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode().strip()
            print(f"[RECV] {addr}: {message}")

            process_command(conn, message)

        except Exception as e:
            print(f"[ERROR] {e}")
            break

    # Cleanup
    with lock:
        for topic in topics:
            if conn in topics[topic]:
                topics[topic].remove(conn)

    if conn in authenticated_clients:
        del authenticated_clients[conn]

    conn.close()
    print(f"[DISCONNECTED] {addr}")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[LISTENING] on {HOST}:{PORT}")

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    secure_server = context.wrap_socket(server, server_side=True)

    while True:
        conn, addr = secure_server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


start_server()