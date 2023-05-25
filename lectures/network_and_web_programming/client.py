import socket

# Client

UDP_IP = "localhost"
UDP_PORT = 8883

MESSAGE = "Hello from the other side"

server = UDP_IP, UDP_PORT
encoding = 'utf-8'
with socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
) as sock:
    data = MESSAGE.encode(encoding)
    bytes_sent = sock.sendto(data, server)
    response, address = sock.recvfrom(1024)
    print(f'Received {response.decode(encoding)!r}')