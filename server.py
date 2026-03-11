import socket
import ssl
import threading

HOST = "0.0.0.0"
PORT = 5000

topics = {}                     
lock = threading.Lock()


def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")

    try:
        while True:
            data = conn.recv(1024).decode().strip()

            if not data:
                break

            parts = data.split(" ", 2)
            command = parts[0]

            # SUBSCRIBE topic
            if command == "SUBSCRIBE":
                topic = parts[1]

                with lock:
                    if topic not in topics:
                        topics[topic] = set()

                    topics[topic].add(conn)

                conn.send(f"SUBSCRIBED {topic}\n".encode())
                print(f"{addr} subscribed to {topic}")

            # PUBLISH topic message
            elif command == "PUBLISH":
                topic = parts[1]
                message = parts[2]

                print(f"[EVENT] {topic}: {message}")

                with lock:
                    if topic in topics:
                        for subscriber in list(topics[topic]):
                            try:
                                subscriber.send(
                                    f"(New Message Received) {topic} {message}\n".encode()
                                )
                            except:
                                topics[topic].remove(subscriber)

            elif command == "EXIT":
                break

            else:
                conn.send("ERROR Invalid command\n".encode())

    except:
        pass

    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr}")


def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(10)

    print(f"Server running on port {PORT}")

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("server.crt", "server.key")

    while True:
        client, addr = sock.accept()

        secure_conn = context.wrap_socket(client, server_side=True)

        thread = threading.Thread(
            target=handle_client,
            args=(secure_conn, addr)
        )
        thread.start()


if __name__ == "__main__":
    start_server()