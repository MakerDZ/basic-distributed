from redis import Redis
from rq import Worker, Queue, Connection
import os
from dotenv import load_dotenv
from multiprocessing import Process
import signal
import sys

# Load environment variables
load_dotenv()

# Default queues if not specified in env
default_queues = ['default']

# Get queues from environment or use defaults
listen_queues = os.getenv('LISTEN_QUEUES', ','.join(default_queues)).split(',')

# Configure Redis connection
redis_conn = Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0)),
    password=os.getenv('REDIS_PASSWORD'),
    ssl=os.getenv('REDIS_SSL', 'false').lower() == 'true',
    ssl_cert_reqs=None  # Required for Upstash Redis
)

# Number of worker processes
NUM_WORKERS = int(os.getenv('NUM_WORKERS', 2))  # Default to 2 workers

def start_worker(worker_id):
    """Start a worker process"""
    print(f"Starting worker {worker_id}")
    with Connection(redis_conn):
        worker = Worker(map(Queue, listen_queues), name=f'worker_{worker_id}')
        worker.work()

def handle_signal(signum, frame):
    """Handle termination signals"""
    print("Shutting down workers...")
    sys.exit(0)

if __name__ == '__main__':
    # Set up signal handlers
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    print(f"Starting {NUM_WORKERS} workers...")
    processes = []

    try:
        # Start worker processes
        for i in range(NUM_WORKERS):
            p = Process(target=start_worker, args=(i+1,))
            p.start()
            processes.append(p)

        # Wait for all processes to complete
        for p in processes:
            p.join()

    except KeyboardInterrupt:
        print("Shutting down...")
        for p in processes:
            p.terminate()
            p.join()
