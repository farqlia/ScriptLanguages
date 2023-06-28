import concurrent.futures
import socket

IP_ADDR = 'localhost'
IP_PORT = 8881
encoding = 'utf-8'


def handle(new_sock, address):
    print(f"Connected from {address}")
    with new_sock:
        while True:
            received = new_sock.recv(1024)
            # Empty result is received if the client wishes
            # to close the connection
            if not received:
                break
            s = received.decode(encoding, errors='replace')
            print(f"Received {s!r}")
            new_sock.sendall(received)
            print(f"Echo: {s!r}")
    print(f"Disconnected from {address}")


with socket.socket(socket.AF_INET, # IPv4,
                   socket.SOCK_STREAM # TCP
                 ) as servsock:
    servsock.bind((IP_ADDR, IP_PORT))
    # There can be up to 5 queued, unaccepted connections
    # before server starts to refuse further connections
    servsock.listen(5)
    print(f"Serving at {servsock.getsockname()}")
    with concurrent.futures.ThreadPoolExecutor(20) as e:
        while True:
            # Awaits an incoming client connection
            # When such a request arrives, a new socket
            # object is created whose other endpoint is the
            # client program
            new_sock, address = servsock.accept()
            # This does not block, but returns instance of Future
            e.submit(handle, new_sock, address)