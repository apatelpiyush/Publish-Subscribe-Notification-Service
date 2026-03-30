import socket
import ssl
import threading

HOST = "0.0.0.0"
PORT = 5000

topics = {}               
client_subscriptions = {}   
lock = threading.Lock()


def send_line(conn, msg):
    conn.send((msg + "\n").encode())


def remove_client(conn):
    with lock:
        subs = client_subscriptions.get(conn, set())

        for topic in subs:
            if topic in topics:
                topics[topic].discard(conn)

        client_subscriptions.pop(conn, None)


def print_topics():
    with lock:
        if not topics:
            print("[TOPICS] none")
            return

        summary = " | ".join(
            f"{t}:{len(s)}" for t, s in topics.items()
        )

        print("[TOPICS]", summary)


def handle_client(conn, addr):

    print("[CONNECTED]", addr)

    client_subscriptions[conn] = set()

    buffer = ""

    try:
        while True:

            data = conn.recv(1024)

            if not data:
                break

            buffer += data.decode()

            while "\n" in buffer:

                line, buffer = buffer.split("\n", 1)
                parts = line.strip().split(" ", 2)

                command = parts[0]

                # -------------------------
                # SUBSCRIBE
                # -------------------------
                if command == "SUBSCRIBE":

                    if len(parts) < 2:
                        send_line(conn, "ERROR Missing topic")
                        continue

                    topic = parts[1]

                    with lock:

                        # check if topic exists
                        if topic not in topics:
                            send_line(conn, "ERROR Topic does not exist")
                            continue

                        topics[topic].add(conn)
                        client_subscriptions[conn].add(topic)

                    send_line(conn, f"SUBSCRIBED = [{topic}]")

                    print(addr, "subscribed to", topic)
                    print_topics()

                # -------------------------
                # CREATE
                # -------------------------
                elif command == "CREATE":

                    if len(parts) < 2:
                        send_line(conn, "ERROR Missing topic")
                        continue

                    topic = parts[1]

                    with lock:
                        if topic not in topics:
                            topics[topic] = set()

                    send_line(conn, f"CREATED [{topic}]")
                    print("[CREATED]", topic)
                    print_topics()

                # -------------------------
                # LIST
                # -------------------------
                elif command == "LIST":

                    with lock:
                        if not topics:
                            send_line(conn, "TOPICS none")
                        else:
                            topic_list = ", ".join(topics.keys())
                            send_line(conn, f"TOPICS = [{topic_list}]")
                # -------------------------
                # SUBS
                # -------------------------

                elif command == "SUBS":

                    with lock:
                        subs = client_subscriptions.get(conn, set())

                    if not subs:
                        send_line(conn, "SUBSCRIBED none")
                    else:
                        send_line(conn, "SUBSCRIBED " + ", ".join(subs))

                # -------------------------
                # PUBLISH
                # -------------------------
                elif command == "PUBLISH":

                    if len(parts) < 3:
                        send_line(conn, "ERROR Missing topic/message")
                        continue

                    topic = parts[1]
                    message = parts[2]

                    print("[EVENT]", topic, ":", message)

                    with lock:
                        if topic not in topics:
                            topics[topic] = set()

                        subscribers = list(topics[topic])

                    for sub in subscribers:
                        try:
                            send_line(sub, f"[{topic.upper()}] {message}")
                        except:
                            remove_client(sub)

                # -------------------------
                # EXIT
                # -------------------------
                elif command == "EXIT":
                    send_line(conn, "BYE")
                    return

                else:
                    send_line(conn, "ERROR Invalid command")

    except:
        pass

    finally:
        remove_client(conn)
        conn.close()

        print("[DISCONNECTED]", addr)
        print_topics()


def start_server():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind((HOST, PORT))
    sock.listen(10)

    print("Server running on port", PORT)

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