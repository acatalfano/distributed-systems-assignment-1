from datetime import datetime
import time
import zmq

port = "5556"

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:" + port)

while True:
    socket.send_string("Time Sent: " + str(datetime.now()))
    time.sleep(1)