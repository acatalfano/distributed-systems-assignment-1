import sys
from typing import Callable
from app.client.host import Host
from time import sleep

id = sys.argv[1]

notify: Callable[[str, str], None] =\
    lambda topic, message: print(f'{topic}: {message}')
sub = Host(notify)
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
