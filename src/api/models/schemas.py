from pydantic import BaseModel
from typing import Optional

class SearchRequest(BaseModel):
    query: str
    song_limit: Optional[int] = None

class ArtistDownloadRequest(BaseModel):
    artist_url: Optional[str] = None
    artist_name: Optional[str] = None
    limit: Optional[int] = None
    song_limit: Optional[int] = None
    max_album_length: Optional[int] = None

class JobResponse(BaseModel):
    message: str
    job_id: str
    status: str
