from datetime import datetime
import time
import zmq

port = "5559"

context = zmq.Context()
socket = context.socket(zmq.PUB)
#Pub socket now 'connects' to a port rather than being bound to it; broker owns the port
socket.connect("tcp://localhost:" + port)

while True:
    socket.send_string("Time Sent: " + str(datetime.now()))
    time.sleep(1)