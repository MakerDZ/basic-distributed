from redis import Redis
from rq import Worker, Queue, Connection
import os
from dotenv import load_dotenv
from multiprocessing import Process
import signal
import sys
import random

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
    password=os.getenv('REDIS_PASSWORD', None) or None,
    ssl=os.getenv('REDIS_SSL', 'false').lower() == 'true',
    ssl_cert_reqs=None  # For Upstash or self-signed certs
)

# Number of worker processes (configurable via .env)
NUM_WORKERS = int(os.getenv('NUM_WORKERS', 2))  # default to 2

def start_worker(worker_id):
    """Start a uniquely named worker process"""
    unique_worker_name = f"worker_{worker_id}_{os.getpid()}_{random.randint(1000, 9999)}"
    print(f"🚀 Starting {unique_worker_name}")
    with Connection(redis_conn):
        worker = Worker(map(Queue, listen_queues), name=unique_worker_name)
        worker.work()

def handle_signal(signum, frame):
    """Gracefully handle Ctrl+C or termination signals"""
    print("👋 Shutting down workers...")
    sys.exit(0)

if __name__ == '__main__':
    # Set up signal handlers for Ctrl+C / kill
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    print(f"🔧 Booting up {NUM_WORKERS} worker(s)...\n")
    processes = []

    try:
        # Start N worker processes
        for i in range(NUM_WORKERS):
            p = Process(target=start_worker, args=(i+1,))
            p.start()
            processes.append(p)

        # Wait for all workers to complete (runs forever)
        for p in processes:
            p.join()

    except KeyboardInterrupt:
        print("🛑 Manual shutdown detected.")
        for p in processes:
            p.terminate()
            p.join()
