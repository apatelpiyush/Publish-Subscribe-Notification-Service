import socket
import ssl
import threading

HOST = "172.24.155.31"
PORT = 5000


def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print("\nNotification:", msg)
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

    threading.Thread(
        target=receive_messages,
        args=(secure_sock,),
        daemon=True
    ).start()

    while True:
        topic = input("Enter topic to subscribe: ")

        cmd = f"SUBSCRIBE {topic}"
        secure_sock.send((cmd + "\n").encode())


if __name__ == "__main__":
    main()