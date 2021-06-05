from app.client.host import Host
import sys

id = sys.argv[1]
pub = Host()
pub.add_publisher(id)

if id == '1':
    input('publish(1, x, first message x)')
    pub.publish(id=id, topic='x', value='first message x')
    input('publish(1, y, first message y)')
    pub.publish(id=id, topic='y', value='first message y')
elif id == '2':
    input('publish(2, x, second message x)')
    pub.publish(id=id, topic='x', value='second message y')
elif id == '3':
    input('publish(3, a, first message a)')
    pub.publish(id=id, topic='a', value='first message a')
    input('publish(3, z, first message z)')
    pub.publish(id=id, topic='z', value='first message z')
