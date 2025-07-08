# Setup Guide

## Requirements
- Python 3.8+
- Redis

## Quick Setup

1. **Install Redis**
```bash
# macOS
brew install redis
brew services start redis

# Ubuntu
sudo apt-get install redis-server
sudo service redis-server start

# Windows
Download from https://github.com/microsoftarchive/redis/releases
```

2. **Python Setup**
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
.\venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```

3. **Environment Setup**
Create `.env` file with:
```ini
# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# Queues
LISTEN_QUEUES=default,heavy,fast
QUEUE_NAME=default
```

## Running

1. **Start API Server**
```bash
uvicorn app.api:app --reload
```
API will run on http://localhost:8000

2. **Start Worker**
```bash
python worker_runner.py
```

## Testing

Submit a job:
```bash
curl -X POST "http://localhost:8000/submit?video_path=test.mp4"
```

Check status:
```bash
curl "http://localhost:8000/status/{job_id}"
```

## Troubleshooting

- **Redis not connecting**: Make sure Redis is running (`redis-cli ping`)
- **Worker not processing**: Check if worker is running
- **API not starting**: Check if port 8000 is free 