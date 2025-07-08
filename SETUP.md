# Setup Guide

## Requirements
- Python 3.8+
- Upstash Redis account (or any Redis service)

## Quick Setup

1. **Set Environment Variables**
```ini
# Redis
REDIS_HOST=your-redis-host
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password
REDIS_SSL=true

# Queues (optional)
LISTEN_QUEUES=default
QUEUE_NAME=default
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

- **Redis not connecting**: Check your Redis credentials and SSL settings
- **Worker not processing**: Check if worker is running
- **API not starting**: Check if port 8000 is free 