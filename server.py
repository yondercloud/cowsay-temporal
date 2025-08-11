from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from temporalio.client import Client
from workflow import CowsayWorkflow
import uuid
import os


class CowsayRequest(BaseModel):
    message: str


class CowsayResponse(BaseModel):
    workflow_id: str
    result: str


app = FastAPI(title="Cowsay Temporal API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/cowsay", response_model=CowsayResponse)
async def run_cowsay_workflow(request: CowsayRequest):
    try:
        temporal_host = os.getenv("TEMPORAL_HOST", "localhost:7233")
        client = await Client.connect(temporal_host)
        workflow_id = f"cowsay-{uuid.uuid4()}"
        
        result = await client.execute_workflow(
            CowsayWorkflow.run,
            request.message,
            id=workflow_id,
            task_queue="cowsay-task-queue",
        )
        
        return CowsayResponse(workflow_id=workflow_id, result=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/")
async def read_index():
    return FileResponse("index.html")


@app.get("/index.html")
async def read_index_html():
    return FileResponse("index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)