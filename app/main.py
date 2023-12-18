import socket
import threading
import argparse
from os import listdir
from os.path import isfile, join


class HttpServer:
    def __init__(self, directory):
        self.directory = directory if directory else ""

    def run(self):
        server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

        try:
            while True:
                conn, address = server_socket.accept()  # wait for client

                thread = threading.Thread(target=self.handle_request, args=(conn,))
                thread.daemon = True
                thread.start()
        finally:
            conn.close()

    def send_response(self, conn, status, response, content_type="text/plain"):
        conn.sendall(f"HTTP/1.1 {status}\r\n".encode())
        conn.sendall(f"Content-Type: {content_type}\r\n".encode())
        conn.sendall(f"Content-Length: {len(response)}\r\n\r\n".encode())
        conn.sendall(f"{response}\r\n\r\n".encode())

    def handle_request(self, conn):
        message = conn.recv(1024).decode()

        request = message.split("\r\n")

        start_line = request[0]
        http_method, path, http_version = start_line.split(" ")

        headers = {}
        for i in range(1, len(request) - 1):
            line = request[i]
            if ": " in line:
                header, value = line.split(": ")
                headers[header] = value

        if path == "/":
            conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

        elif path.startswith("/echo"):
            response = path.removeprefix("/echo/")
            self.send_response(conn, "200 OK", response)

        elif path == ("/user-agent"):
            response = headers["User-Agent"]
            self.send_response(conn, "200 OK", response)

        elif path.startswith("/files"):
            filename = path.removeprefix("/files/")
            files = [
                f for f in listdir(self.directory) if isfile(join(self.directory, f))
            ]

            if filename in files:
                file_content = ""
                with open(join(self.directory, filename), "r") as content_file:
                    file_content = content_file.read()
                self.send_response(
                    conn, "200 OK", file_content, "application/octet-stream"
                )
            else:
                self.send_response(conn, "404 Not Found", "")

        else:
            self.send_response(conn, "404 Not Found", "")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory")
    args = parser.parse_args()

    directory = args.directory

    server = HttpServer(directory)
    server.run()


if __name__ == "__main__":
    main()
