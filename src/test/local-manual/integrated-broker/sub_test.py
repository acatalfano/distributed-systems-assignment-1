import sys
from app.client.subscriber import Subscriber

id = sys.argv[1]

sub = Subscriber(id)

if id == '4':
    sub.subscribe('x')
    sub.subscribe('y')
    sub.subscribe('z')
elif id == '5':
    sub.subscribe('x')
elif id == '6':
    sub.subscribe('z')

sub.recv_message()
