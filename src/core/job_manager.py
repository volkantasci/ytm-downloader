import multiprocessing
import uuid
import time
import sys
import traceback
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime

class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Job:
    def __init__(self, job_type: str, target: str, args: tuple = (), kwargs: dict = {}):
        self.id: str = str(uuid.uuid4())
        self.job_type: str = job_type
        self.target: str = target
        self.status: JobStatus = JobStatus.QUEUED
        self.created_at: float = time.time()
        self.started_at: Optional[float] = None
        self.completed_at: Optional[float] = None
        self.process: Optional[multiprocessing.Process] = None
        # Queue for sending logs from child process to parent
        self.log_queue: multiprocessing.Queue = multiprocessing.Queue()
        self.logs: List[str] = []
        self.args = args
        self.kwargs = kwargs
        self.error: Optional[str] = None

    def to_dict(self):
        return {
            "id": self.id,
            "job_type": self.job_type,
            "target": self.target,
            "status": self.status,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "error": self.error
        }

class LogCapture:
    def __init__(self, queue):
        self.queue = queue

    def write(self, msg):
        if msg.strip(): # Avoid empty newlines
            self.queue.put(msg)

    def flush(self):
        pass

def worker_wrapper(job_id, queue, func, *args, **kwargs):
    """
    Wrapper to run in the separate process.
    Redirects stdout/stderr to the queue.
    """
    # Redirect stdout/stderr
    sys.stdout = LogCapture(queue)
    sys.stderr = LogCapture(queue)
    
    print(f"Job {job_id} started processing.")
    
    try:
        func(*args, **kwargs)
        print(f"Job {job_id} completed successfully.")
        queue.put("JOB_COMPLETE")
    except Exception as e:
        print(f"Job {job_id} failed: {e}")
        traceback.print_exc()
        queue.put("JOB_FAILED")
        queue.put(str(e))

class JobManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JobManager, cls).__new__(cls)
            cls._instance._init()
        return cls._instance

    def _init(self):
        self.jobs: Dict[str, Job] = {}
        # We need a way to monitor queues. 
        # In a real heavy app, we might use a dedicated thread/process for monitoring.
        # For now, we'll rely on polling or on-demand checking when client asks for logs.
        # BUT, to detect completion/failure properly without client interaction, 
        # we strictly need a background thread monitoring active jobs.
        pass

    def create_job(self, job_type: str, target: str, func, *args, **kwargs) -> str:
        job = Job(job_type, target, args, kwargs)
        self.jobs[job.id] = job
        
        # Start immediately for now (simple queue)
        self._start_job(job, func)
        return job.id

    def _start_job(self, job: Job, func):
        job.status = JobStatus.RUNNING
        job.started_at = time.time()
        
        # Spawn process
        # Note: We must pass simple args. If func is complex or not picklable, this fails.
        # Our download functions are top-level module functions, so they should picklable.
        job.process = multiprocessing.Process(
            target=worker_wrapper,
            args=(job.id, job.log_queue, func, *job.args),
            kwargs=job.kwargs
        )
        job.process.start()

    def get_job(self, job_id: str) -> Optional[Job]:
        return self.jobs.get(job_id)

    def list_jobs(self) -> List[Job]:
        # Sort by reverse created_at
        return sorted(self.jobs.values(), key=lambda x: x.created_at, reverse=True)

    def cancel_job(self, job_id: str) -> bool:
        job = self.jobs.get(job_id)
        if not job:
            return False
        
        if job.status == JobStatus.RUNNING and job.process and job.process.is_alive():
            job.process.terminate()
            job.status = JobStatus.CANCELLED
            job.completed_at = time.time()
            job.logs.append("Job cancelled by user.")
            return True
        return False

    def update_job_logs(self, job_id: str):
        """
        Reads from queue and updates job.logs.
        Should be called periodically or before returning logs.
        Also checks process status.
        """
        job = self.jobs.get(job_id)
        if not job:
            return

        # Drain queue
        while not job.log_queue.empty():
            try:
                msg = job.log_queue.get_nowait()
                if msg == "JOB_COMPLETE":
                    job.status = JobStatus.COMPLETED
                    job.completed_at = time.time()
                elif msg == "JOB_FAILED":
                    job.status = JobStatus.FAILED
                    job.completed_at = time.time()
                    # Next msg might be error details, handled by loop
                else:
                    job.logs.append(msg)
            except:
                break
        
        # Check process liveness as fallback
        if job.status == JobStatus.RUNNING and job.process:
            if not job.process.is_alive():
                # Process died but maybe didn't send complete signal (e.g. segfault or killed)
                # Give it a moment for queue to drain in next cycle? 
                # For now, mark as completed if not failed/cancelled?
                # Let's assume if it's dead and status is still RUNNING, something weird happened 
                # OR we just haven't processed the completion msg yet. 
                # We'll leave it unless it stays stale.
                pass

# Global instance
job_manager = JobManager()
