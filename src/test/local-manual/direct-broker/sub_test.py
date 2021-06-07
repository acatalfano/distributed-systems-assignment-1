import sys
from app.client.host import Host
from time import sleep

id = sys.argv[1]
sub = Host()
sub.add_subscriber(id)

if id == '4':
    sub.subscribe(id, 'x')
    sub.subscribe(id, 'y')
    sleep(5)
    sub.subscribe(id, 'z')

elif id == '5':
    sub.subscribe(id, 'x')

elif id == '6':
    sub.subscribe(id, 'z')
