from fastapi import APIRouter, HTTPException
from ..models.schemas import SearchRequest, ArtistDownloadRequest, JobResponse
from src.core.downloader import download_search_query, download_artist_albums
from src.core.job_manager import job_manager

router = APIRouter()

@router.post("/search", response_model=JobResponse)
async def search_download(request: SearchRequest):
    job_id = job_manager.create_job(
        "search", 
        request.query, 
        download_search_query, 
        request.query, 
        request.song_limit
    )
    return JobResponse(message="Search download started", job_id=job_id, status="queued")

@router.post("/artist", response_model=JobResponse)
async def artist_download(request: ArtistDownloadRequest):
    if not request.artist_url and not request.artist_name:
        raise HTTPException(status_code=400, detail="Either artist_url or artist_name must be provided")
    
    job_id = job_manager.create_job(
        "artist",
        request.artist_name or request.artist_url,
        download_artist_albums,
        request.artist_url,
        request.artist_name,
        limit=request.limit,
        song_limit=request.song_limit,
        max_album_length=request.max_album_length
    )
    return JobResponse(message="Artist download started", job_id=job_id, status="queued")
