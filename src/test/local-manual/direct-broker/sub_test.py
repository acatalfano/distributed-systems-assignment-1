import sys
from src.app.client.host import Host

id = sys.argv[1]
sub = Host()
sub.add_subscriber(id)

# TODO: implement Subscriber for direct broker; this may be redundant but I'm not sure yet