import time
import zmq
import sys

port = "5560"

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

pub_server = sys.argv[1] if len(sys.argv) > 1 else "localhost"
print("Connecting to broker")
socket.connect("tcp://" + pub_server + ':' + port)

socket.setsockopt_string(zmq.SUBSCRIBE, '')

while True:
    msg = socket.recv_string()
    print(msg)
    time.sleep(1)
