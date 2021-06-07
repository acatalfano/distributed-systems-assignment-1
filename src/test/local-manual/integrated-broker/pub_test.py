import sys
from app.client.host import Host

host_id = sys.argv[1]

pub = Host()
pub.add_publisher(host_id)

if host_id == '1':
    input('publish(1, x, first message x)')
    pub.publish(id=host_id, topic='x', value='first message x')
    input('publish(1, y, first message y)')
    pub.publish(id=host_id, topic='y', value='first message y')
elif host_id == '2':
    input('publish(2, x, second message x)')
    pub.publish(id=host_id, topic='x', value='second message x')
elif host_id == '3':
    input('publish(3, a, first message a)')
    pub.publish(id=host_id, topic='a', value='first message a')
    input('publish(3, z, first message z)')
    pub.publish(id=host_id, topic='z', value='first message z')

print('done')
