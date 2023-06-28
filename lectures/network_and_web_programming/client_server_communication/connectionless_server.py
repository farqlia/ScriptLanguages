import socket

UDP_IP = 'localhost'
UDP_PORT = 8883

with socket.socket(socket.AF_INET,
                   socket.SOCK_DGRAM) as sock:
    sock.bind((UDP_IP, UDP_PORT))
    print(f"Serving at {UDP_IP}:{UDP_PORT}")

    # There is no way to stop the server other than interrupting it
    while True:
        data, sender_addr = sock.recvfrom(1024)
        print(f"Received {data!r} from {sender_addr}")
        bytes_sent = sock.sendto(data, sender_addr)
        print(f"Sent {data!r} ({bytes_sent}/{len(data)}) "
              f"to {sender_addr}")