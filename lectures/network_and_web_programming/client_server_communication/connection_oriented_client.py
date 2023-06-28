import socket

IP_ADDR = 'localhost'
IP_PORT = 8881
MESSAGE = """\
A few lines of text
including non-ASCII characters: €£
to test the operation
of both server
and client."""

encoding = 'utf-8'

with socket.socket(socket.AF_INET,
                   socket.SOCK_STREAM # TCP
                  ) as sock:
    sock.connect((IP_ADDR, IP_PORT))
    print(f"Connected to {IP_ADDR}:{IP_PORT}")
    for line in MESSAGE.splitlines():
        # Text must be encoded before transmission and
        # decoded upon reception
        data = line.encode(encoding)
        sock.sendall(data)
        print(f"Sent {data!r} {len(data)}")
        response, address = sock.recvfrom(1024) # buffer size = 1024
        print(f"Received {response.decode(encoding)!r} from {address}")

    print("Disconnected from server")