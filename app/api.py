from fastapi import FastAPI
from redis import Redis
from rq import Queue
from rq.job import Job
from app.worker_job import process_video
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()
redis_conn = Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0)),
    password=os.getenv('REDIS_PASSWORD'),
    ssl=os.getenv('REDIS_SSL', 'false').lower() == 'true',
    ssl_cert_reqs=None  # Required for Upstash Redis
)
q = Queue(os.getenv('QUEUE_NAME', 'default'), connection=redis_conn)

# 1. Submit a new job
@app.post("/submit")
def submit_job(video_path: str):  # can use Form/File later
    job = q.enqueue(process_video, video_path)
    return {"status": "queued", "job_id": job.id}

# 2. Check job status
@app.get("/status/{job_id}")
def check_status(job_id: str):
    try:
        job = Job.fetch(job_id, connection=redis_conn)
        return {
            "job_id": job.id,
            "status": job.get_status(),
            "enqueued_at": str(job.enqueued_at),
            "started_at": str(job.started_at) if job.started_at else None,
            "ended_at": str(job.ended_at) if job.ended_at else None
        }
    except Exception:
        return {"error": "Job not found"}

# 3. Get job result (after done)
@app.get("/result/{job_id}")
def get_result(job_id: str):
    try:
        job = Job.fetch(job_id, connection=redis_conn)
        if job.is_finished:
            return {"job_id": job.id, "result": job.result}
        elif job.is_failed:
            return {"job_id": job.id, "status": "failed", "error": str(job.exc_info)}
        else:
            return {"job_id": job.id, "status": job.get_status()}
    except Exception:
        return {"error": "Job not found"}
