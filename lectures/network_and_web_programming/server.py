import socket

# Serwer

UDP_IP = "localhost"
UDP_PORT = 8883

with socket.socket(
    socket.AF_INET, socket.SOCK_DGRAM
) as sock:
    sock.bind((UDP_IP, UDP_PORT))
    while True:
        data, sender_addr = sock.recvfrom(1024)
        bytes_sent = sock.sendto(data, sender_addr)
        print(f'Sent {data!r}')
