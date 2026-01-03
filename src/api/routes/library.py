from fastapi import APIRouter, Query, HTTPException
from ..models.schemas import JobResponse
from src.core.downloader import scan_and_fix_library
from src.core.job_manager import job_manager
import os
from typing import List, Dict

router = APIRouter()

BASE_MUSIC_DIR = "/app/music"

@router.post("/scan", response_model=JobResponse)
async def scan_library():
    job_id = job_manager.create_job(
        "library_scan",
        "Full Library",
        scan_and_fix_library
    )
    return JobResponse(message="Library scan started", job_id=job_id, status="queued")

@router.get("/files")
async def list_files(path: str = Query("", description="Relative path from music root")):
    # Security check: prevent directory traversal
    if ".." in path or path.startswith("/"):
        raise HTTPException(status_code=400, detail="Invalid path")
    
    target_path = os.path.join(BASE_MUSIC_DIR, path)
    
    if not os.path.exists(target_path):
         # If root doesn't exist, create it or return empty
         if path == "":
             return []
         raise HTTPException(status_code=404, detail="Path not found")
    
    if not os.path.isdir(target_path):
        raise HTTPException(status_code=400, detail="Not a directory")

    items = []
    try:
        with os.scandir(target_path) as it:
            for entry in it:
                items.append({
                    "name": entry.name,
                    "type": "directory" if entry.is_dir() else "file",
                    "path": os.path.join(path, entry.name),
                    "size": entry.stat().st_size if entry.is_file() else 0
                })
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied")

    # Sort: Directories first, then files
    items.sort(key=lambda x: (x["type"] != "directory", x["name"].lower()))
    
    return items
