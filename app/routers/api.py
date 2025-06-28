from fastapi import APIRouter

router = APIRouter()

@router.get("/data")
def get_data():
    return {"message": "This is a sample data endpoint."}

@router.post("/data")
def post_data():
    return {"message": "Data received"}

