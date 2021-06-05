from src.app.client.publisher.publisher import Publisher
import sys

testId = sys.argv[1]

pub = Publisher(testId)

if testId == '1':
    input('publish(1, x, first message x)')
    pub.publish('x', 'first message x')
    input('publish(1, y, first message y)')
    pub.publish('y', 'first message y')
elif testId == '2':
    input('publish(2, x, second message x)')
    pub.publish('x', 'second message x')
elif testId == '3':
    input('publish(3, z, first message z)')
    pub.publish('z', 'first message z')

print('done')
