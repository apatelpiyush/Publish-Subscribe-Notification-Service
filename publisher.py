import socket
import ssl

HOST = "127.0.0.1"
PORT = 5000


def main():

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_sock = context.wrap_socket(sock, server_hostname="localhost")

    secure_sock.connect((HOST, PORT))

    print("Connected as Publisher")
    print("Commands: list | switch | exit\n")

    topic = None

    while True:

        # choose topic
        if topic is None:

            cmd = input("Topic> ").strip()

            if cmd.lower() == "exit":
                secure_sock.send(b"EXIT\n")
                break

            if cmd.lower() == "list":
                secure_sock.send(b"LIST\n")
                print(secure_sock.recv(1024).decode())
                continue

            if not cmd:
                continue

            topic = cmd
            print("Publishing to topic:", topic)
            continue

        # send message
        msg = input(f"{topic}> ").strip()

        if msg.lower() == "exit":
            secure_sock.send(b"EXIT\n")
            break

        if msg.lower() == "switch":
            topic = None
            continue

        if msg.lower() == "list":
            secure_sock.send(b"LIST\n")
            print(secure_sock.recv(1024).decode())
            continue

        if not msg:
            continue

        secure_sock.send(f"PUBLISH {topic} {msg}\n".encode())

    secure_sock.close()


if __name__ == "__main__":
    main()