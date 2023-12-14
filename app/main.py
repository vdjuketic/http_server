import socket


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, address = server_socket.accept()  # wait for client

    message = conn.recv(1024).decode()

    request = message.split("\r\n")

    start_line = request[0]
    http_method, path, http_version = start_line.split(" ")

    headers = {}
    for line in range(1, len(request) - 1):
        if ": " in line:
            header, value = line.split(": ")
            headers[header] = value

    if path == "/":
        conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

    elif path.startswith("/echo"):
        response = path.removeprefix("/echo/")
        conn.sendall(b"HTTP/1.1 200 OK\r\n")
        conn.sendall(b"Content-Type: text/plain\r\n")
        conn.sendall(f"Content-Length: {len(response)}\r\n\r\n".encode())
        conn.sendall(f"{response}\r\n\r\n".encode())

    elif path == ("/user-agent"):
        print(headers)

    else:
        conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

    conn.close()


if __name__ == "__main__":
    main()
