from fastapi import FastAPI
from pydantic import BaseModel
from agent_engine import start_agent_run, approve_and_push
import uvicorn
import os

app = FastAPI()

class BugReport(BaseModel):
    issue_id: str
    description: str

@app.get("/")
def health_check():
    return {"status": "Agent is online"}

@app.post("/start_run")
def start_run(report: BugReport):
    # This endpoint triggers the Phase 1 & 2 (RAG + Loop)
    status = start_agent_run(report.issue_id, report.description)
    return {"message": status}

@app.post("/approve/{issue_id}")
def approve(issue_id: str):
    # This endpoint triggers Phase 3 (Human-in-the-Loop)
    status = approve_and_push(issue_id)
    return {"message": status}

if __name__ == "__main__":
    # Cloud Run provides the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
