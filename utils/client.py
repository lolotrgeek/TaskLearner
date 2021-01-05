import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
# server_address = ('169.254.2.1', 10000)
server_address = ('169.254.2.68', 10000)

print(sys.stderr, 'connecting to %s port %s' % server_address)
sock.connect(server_address)

try:
    # Send data
    message = bytearray([0, 0 & 0xff, 0 & 0xff, 0 & 0xff])
    print(sys.stderr, 'sending "%s"' % message)
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print(sys.stderr, 'received "%s"' % data)

finally:
    print(sys.stderr, 'closing socket')
    sock.close()

