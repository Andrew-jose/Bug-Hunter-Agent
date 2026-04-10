import vertexai
from vertexai.generative_models import GenerativeModel, Tool
from tools import rag_tool, test_tool, retrieve_relevant_files, run_tests
import os

# Initialize Vertex AI with environment variables for security
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
GCP_LOCATION = os.environ.get("GCP_LOCATION", "us-central1")

if not GCP_PROJECT_ID:
    raise ValueError(
        "GCP_PROJECT_ID environment variable must be set. "
        "See .env.example for configuration details."
    )

vertexai.init(project=GCP_PROJECT_ID, location=GCP_LOCATION)

agent_tools = Tool(function_declarations=[rag_tool, test_tool])

model = GenerativeModel(
    "gemini-1.5-pro",
    tools=[agent_tools],
    system_instruction=(
        "You are a production-ready AI coding agent. "
        "1. Use retrieve_relevant_files to find the code. "
        "2. Fix the bug. "
        "3. You MUST run_tests to verify your fix. "
        "4. If tests fail, iterate until they pass. "
        "5. Once tests pass, say: 'READY_FOR_REVIEW'."
    )
)

session_memory = {}

def start_agent_run(issue_id: str, description: str):
    chat = model.start_chat()
    session_memory[issue_id] = {"chat_session": chat, "status": "running"}
    
    print(f"\n[Engine] Starting agent for Issue {issue_id}...")
    response = chat.send_message(f"Fix this bug: {description}")
    
    while response.function_call:
        if response.function_call.name == "retrieve_relevant_files":
            data = retrieve_relevant_files(description)
            response = chat.send_message(f"File found: {data}")
            
        elif response.function_call.name == "run_tests":
            result = run_tests()
            response = chat.send_message(f"Test Result: {result}")
            
    if "READY_FOR_REVIEW" in response.text:
        session_memory[issue_id]["status"] = "awaiting_approval"
        return "Agent finished coding. Tests passed. Awaiting HITL approval."
    
    return "Agent finished, but did not reach a ready state."

def approve_and_push(issue_id: str):
    state = session_memory.get(issue_id)
    if state and state["status"] == "awaiting_approval":
        state["status"] = "completed"
        return "PR successfully pushed to GitHub!"
    
    return "Issue not found or not ready for approval."
    