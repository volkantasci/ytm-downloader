from fastapi import APIRouter
from ..models.schemas import JobResponse
from src.core.downloader import scan_and_fix_library
from src.core.job_manager import job_manager

router = APIRouter()

@router.post("/scan", response_model=JobResponse)
async def scan_library():
    job_id = job_manager.create_job(
        "library_scan",
        "Full Library",
        scan_and_fix_library
    )
    return JobResponse(message="Library scan started", job_id=job_id, status="queued")
