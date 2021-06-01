from app.client.publisher import Publisher
import sys

id = sys.argv[1]

pub = Publisher(id)

if id == '1':
    input('publish(1, x, first message x)')
    pub.publish('x', 'first message x')
    input('publish(1, y, first message y)')
    pub.publish('y', 'first message y')
elif id == '2':
    input('publish(2, x, second message x)')
    pub.publish('x', 'second message x')
elif id == '3':
    input('publish(3, z, first message z)')
    pub.publish('z', 'first message z')

print('done')
