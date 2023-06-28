import socket

UDP_IP = 'localhost'
UDP_PORT = 8883
MESSAGE = """\
This is a bunch of lines, each
of which will be sent in a single
UDP datagram. No error detection
or correction will occur.
Crazy bananas! £€ should go through."""

server = UDP_IP, UDP_PORT
encoding = 'utf-8'

with socket.socket(socket.AF_INET, # IPv4 Address Family
                   socket.SOCK_DGRAM, # Use UDP
                  ) as sock:
    for line in MESSAGE.splitlines():
        data = line.encode(encoding)
        bytes_sent = sock.sendto(data, server)
        print(f"Sent {bytes_sent} bytes of {len(data)} to {server}")
        response, address = sock.recvfrom(1024) # buffer size = 1024
        print(f"Received {response.decode(encoding)!r} from {address}")

    print("Disconnected from server")


