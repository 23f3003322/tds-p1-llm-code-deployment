from fastapi import FastAPI, HTTPException, status, Request
from models import TaskRequest
from utils import validate_secret
app = FastAPI()

@app.post("/handle-task")
async def handle_task(request: TaskRequest):
    if not validate_secret(request.secret):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid secret",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Proceed with further task processing here
    return {"status": "success"}




@app.get("/")
def read_root():
    return {"Hello": "World"}   
