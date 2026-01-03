from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import downloads, library, jobs

app = FastAPI(title="YTM Downloader API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(downloads.router, prefix="/api/v1/downloads", tags=["Downloads"])
app.include_router(library.router, prefix="/api/v1/library", tags=["Library"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Jobs"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
