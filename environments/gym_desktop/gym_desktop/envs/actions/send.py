import socket
import sys
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection = False
def send(server_address, report):
    global connection
    if connection is False:
        sock.connect(server_address)
        connection = True
    try:
        # Send data
        message = bytearray(report)
        # print(sys.stderr, 'sending "%s"' % message)
        sock.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            # print(sys.stderr, 'received "%s"' % data)

    except:
        print(sys.stderr, 'closing socket')
        sock.close()    