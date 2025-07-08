from redis import Redis
from rq import Worker, Queue, Connection
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default queues if not specified in env
default_queues = ['default']  # you can use 'heavy', 'fast', etc. later

# Get queues from environment or use defaults
listen_queues = os.getenv('LISTEN_QUEUES', ','.join(default_queues)).split(',')

# Configure Redis connection
redis_conn = Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0)),
    password=os.getenv('REDIS_PASSWORD', None) or None
)

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(map(Queue, listen_queues))
        worker.work()
