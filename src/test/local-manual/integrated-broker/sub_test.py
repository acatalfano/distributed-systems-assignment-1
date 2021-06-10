import sys
import time
from typing import Callable
from app import Host

host_id = sys.argv[1]

notify: Callable[[str, str], None] = lambda topic, message: print(
    f'{topic}: {message}')

sub = Host(notify)
sub.add_subscriber(host_id)

if host_id == '4':
    sub.subscribe(host_id, 'x')
    sub.subscribe(host_id, 'y')
    sub.subscribe(host_id, 'z')
    time.sleep(10)
    print('done sleeping')


elif host_id == '5':
    sub.subscribe(host_id, 'x')
elif host_id == '6':
    sub.subscribe(host_id, 'z')
else:
    print('nothing executed')

# sub.subscribers[host_id].recv_message()
sub.subscribe(host_id, 'a')
print('added a')
