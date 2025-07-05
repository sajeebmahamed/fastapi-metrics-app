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

@router.get("/data/{item_id}")
async def get_data_by_id(item_id: str):
    """
    Get specific data item by ID
    """
    if item_id not in data_store:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {
        "id": item_id,
        "data": data_store[item_id],
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

@router.put("/data/{item_id}")
async def update_data(item_id: str, request: DataRequest):
    """
    Update existing data item
    """
    if item_id not in data_store:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Simulate processing time
    processing_time = random.uniform(0.05, 0.2)
    await asyncio.sleep(processing_time)
    
    # Update data
    data_store[item_id].update({
        "name": request.name,
        "value": request.value,
        "metadata": request.metadata,
        "updated_at": time.time(),
        "processing_time": processing_time
    })
    
    return DataResponse(
        id=item_id,
        message="Data updated successfully",
        timestamp=time.time(),
        data=data_store[item_id]
    )

@router.delete("/data/{item_id}")
async def delete_data(item_id: str):
    """
    Delete data item
    """
    if item_id not in data_store:
        raise HTTPException(status_code=404, detail="Item not found")
    
    deleted_item = data_store.pop(item_id)
    
    return {
        "message": "Data deleted successfully",
        "deleted_item": deleted_item,
        "timestamp": time.time()
    }

@router.get("/data/search/{query}")
async def search_data(query: str):
    """
    Search data by name
    """
    # Simulate search processing
    await asyncio.sleep(0.1)
    
    results = {
        item_id: item_data 
        for item_id, item_data in data_store.items()
        if query.lower() in item_data.get("name", "").lower()
    }
    
    return {
        "query": query,
        "results": results,
        "count": len(results),
        "timestamp": time.time()
    }

@router.get("/slow-endpoint")
async def slow_endpoint():
    """
    Endpoint that simulates slow processing
    Useful for testing latency metrics
    """
    # Simulate slow processing (2-5 seconds)
    processing_time = random.uniform(2.0, 5.0)
    await asyncio.sleep(processing_time)
    
    return {
        "message": "Slow processing completed",
        "processing_time": processing_time,
        "timestamp": time.time()
    }

@router.get("/error-endpoint")
async def error_endpoint():
    """
    Endpoint that randomly generates errors
    Useful for testing error metrics
    """
    # 30% chance of error
    if random.random() < 0.3:
        raise HTTPException(status_code=500, detail="Simulated server error")
    
    return {
        "message": "Request processed successfully",
        "timestamp": time.time()
    }

def background_task(task_name: str):
    """Background task for demonstration"""
    time.sleep(2)
    print(f"Background task '{task_name}' completed")

@router.post("/background-task")
async def create_background_task(background_tasks: BackgroundTasks):
    """
    Create a background task
    """
    task_name = f"task_{int(time.time() * 1000)}"
    background_tasks.add_task(background_task, task_name)
    
    return {
        "message": "Background task created",
        "task_name": task_name,
        "timestamp": time.time()
    }