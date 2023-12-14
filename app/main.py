import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, address = server_socket.accept()  # wait for client

    message = conn.recv(1024).decode()

    request = message.split("\r\n")

    start_line = request[0]
    http_method, path, http_version = start_line.split(" ")

    if path == "/":
        conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    else:
        conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

    conn.close()


if __name__ == "__main__":
    main()
