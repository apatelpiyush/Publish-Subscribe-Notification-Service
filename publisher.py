import socket
import ssl

HOST = "172.24.155.31"
PORT = 5000


def main():

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_sock = context.wrap_socket(sock, server_hostname="localhost")

    secure_sock.connect((HOST, PORT))

    print("Connected as Publisher")

    while True:

        topic = input("Enter topic: ")
        message = input("Enter message: ")

        cmd = f"PUBLISH {topic} {message}"

        secure_sock.send((cmd + "\n").encode())


if __name__ == "__main__":
    main()