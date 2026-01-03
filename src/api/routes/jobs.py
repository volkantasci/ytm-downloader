from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import List, Optional
import asyncio
from src.core.job_manager import job_manager, JobStatus

router = APIRouter()

@router.get("", response_model=List[dict])
async def list_jobs():
    jobs = job_manager.list_jobs()
    return [job.to_dict() for job in jobs]

@router.get("/{job_id}", response_model=dict)
async def get_job(job_id: str):
    job = job_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job.to_dict()

@router.post("/{job_id}/cancel", response_model=dict)
async def cancel_job(job_id: str):
    success = job_manager.cancel_job(job_id)
    if not success:
        raise HTTPException(status_code=400, detail="Job could not be cancelled or not found")
    return {"message": "Job cancelled"}

@router.websocket("/{job_id}/logs")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    await websocket.accept()
    job = job_manager.get_job(job_id)
    
    if not job:
        await websocket.send_text("Job not found")
        await websocket.close()
        return

    last_log_index = 0
    
    try:
        while True:
            # Refresh logs from queue
            job_manager.update_job_logs(job_id)
            
            # Send new logs
            current_logs = job.logs
            if len(current_logs) > last_log_index:
                new_logs = current_logs[last_log_index:]
                for log in new_logs:
                    await websocket.send_text(log)
                last_log_index = len(current_logs)
            
            # Check status
            if job.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
                # Send any remaining logs then close
                job_manager.update_job_logs(job_id)
                current_logs = job.logs
                if len(current_logs) > last_log_index:
                    for log in current_logs[last_log_index:]:
                        await websocket.send_text(log)
                
                await websocket.send_text(f"JOB_STATUS:{job.status.value}")
                await websocket.close()
                break
            
            await asyncio.sleep(0.5)
            
    except WebSocketDisconnect:
        print(f"Client disconnected from job {job_id} logs")
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.close()
        except:
            pass

@router.websocket("")
async def ws_jobs(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            jobs = job_manager.list_jobs()
            await websocket.send_json([job.to_dict() for job in jobs])
            await asyncio.sleep(1) # Broadcast every second
    except WebSocketDisconnect:
        print("Client disconnected from jobs feed")
    except Exception as e:
        print(f"Jobs WebSocket error: {e}")
        try:
            await websocket.close()
        except:
            pass
