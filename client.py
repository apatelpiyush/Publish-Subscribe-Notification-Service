import socket
import ssl
import threading

HOST = "127.0.0.1"
PORT = 5000


def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()

            if not msg:
                break

            print("\n" + msg.strip())

        except:
            break


def main():

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    secure_sock = context.wrap_socket(sock, server_hostname="localhost")

    secure_sock.connect((HOST, PORT))

    print("Connected as Subscriber")
    print("Commands:")
    print("topic name → subscribe")
    print("list → view topics")
    print("subs → view subscribed topics")
    print("exit → quit\n")

    thread = threading.Thread(
        target=receive_messages,
        args=(secure_sock,),
        daemon=True
    )

    thread.start()

    while True:

        cmd = input(">> ").strip().lower()

        if not cmd:
            continue

        if cmd == "list":
            secure_sock.send(b"LIST\n")

        elif cmd == "subs":
            secure_sock.send(b"SUBS\n")

        elif cmd == "exit":
            secure_sock.send(b"EXIT\n")
            break

        else:
            secure_sock.send(f"SUBSCRIBE {cmd}\n".encode())

    secure_sock.close()


if __name__ == "__main__":
    main()