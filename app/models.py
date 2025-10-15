from pydantic import BaseModel

class TaskRequest(BaseModel):
    secret: str
