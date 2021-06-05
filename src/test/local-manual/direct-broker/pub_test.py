from src.app.client.publisher.publisher import Publisher
import sys

testId = sys.argv[1]
pub = Publisher(testId)

# TODO: implement Publisher for direct broker; this may be redundant but I'm not sure yet