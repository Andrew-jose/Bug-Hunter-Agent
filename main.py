from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent_engine import start_agent_run, approve_and_push
import uvicorn
import os
import logging

# Configure logging
logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Bug Hunter AI Agent",
    description="Autonomous bug detection and fixing with Human-in-the-Loop approval",
    version="1.0.0"
)

class BugReport(BaseModel):
    issue_id: str
    description: str

@app.get("/")
def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "online",
        "service": "Bug Hunter AI Agent",
        "version": "1.0.0"
    }

@app.post("/start_run")
def start_run(report: BugReport):
    """
    Initiates autonomous bug hunting workflow (RAG + AI Loop).
    
    Args:
        report: Bug report containing issue_id and description
        
    Returns:
        Status message indicating workflow state
    """
    try:
        # Validate input
        if not report.issue_id.strip():
            raise HTTPException(status_code=400, detail="issue_id cannot be empty")
        if not report.description.strip():
            raise HTTPException(status_code=400, detail="description cannot be empty")
        
        logger.info(f"Starting agent run for issue: {report.issue_id}")
        status = start_agent_run(report.issue_id, report.description)
        
        logger.info(f"Agent run completed for issue: {report.issue_id}")
        return {
            "success": True,
            "issue_id": report.issue_id,
            "message": status
        }
        
    except ValueError as e:
        logger.error(f"Validation error for issue {report.issue_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error in start_run for issue {report.issue_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error. Please check logs for details."
        )

@app.post("/approve/{issue_id}")
def approve(issue_id: str):
    """
    Human-in-the-Loop approval endpoint. Triggers code merge after review.
    
    Args:
        issue_id: The issue ID to approve
        
    Returns:
        Status of the approval and merge operation
    """
    try:
        if not issue_id.strip():
            raise HTTPException(status_code=400, detail="issue_id cannot be empty")
        
        logger.info(f"Processing approval for issue: {issue_id}")
        status = approve_and_push(issue_id)
        
        # Check if approval was successful
        if "not found" in status.lower() or "not ready" in status.lower():
            logger.warning(f"Approval failed for issue {issue_id}: {status}")
            raise HTTPException(status_code=404, detail=status)
        
        logger.info(f"Successfully approved issue: {issue_id}")
        return {
            "success": True,
            "issue_id": issue_id,
            "message": status
        }
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    
    except Exception as e:
        logger.error(f"Unexpected error in approve for issue {issue_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error. Please check logs for details."
        )

if __name__ == "__main__":
    # Cloud Run provides the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting Bug Hunter Agent on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
    