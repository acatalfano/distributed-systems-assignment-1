import sys
import time
from app.client.host import Host

host_id = sys.argv[1]

sub = Host()
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
