from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional
import time
import random
import asyncio

router = APIRouter()

# Data models
class DataRequest(BaseModel):
    name: str
    value: int
    metadata: Optional[Dict[str, Any]] = None

class DataResponse(BaseModel):
    id: str
    message: str
    timestamp: float
    data: Optional[Dict[str, Any]] = None

# In-memory storage for demo
data_store = {}

@router.get("/data")
async def get_data():
    """
    Sample data retrieval endpoint
    Returns all stored data
    """
    return {
        "message": "Data retrieved successfully",
        "count": len(data_store),
        "data": data_store,
        "timestamp": time.time()
    }

@router.post("/data")
async def post_data(request: DataRequest):
    """
    Sample data processing endpoint
    Simulates data processing with variable delay
    """
    # Simulate processing time
    processing_time = random.uniform(0.1, 0.5)
    await asyncio.sleep(processing_time)
    
    # Generate unique ID
    item_id = f"item_{int(time.time() * 1000)}"
    
    # Store data
    data_store[item_id] = {
        "name": request.name,
        "value": request.value,
        "metadata": request.metadata,
        "created_at": time.time(),
        "processing_time": processing_time
    }
    
    return DataResponse(
        id=item_id,
        message="Data processed successfully",
        timestamp=time.time(),
        data={
            "name": request.name,
            "value": request.value,
            "processing_time": processing_time
        }
    )