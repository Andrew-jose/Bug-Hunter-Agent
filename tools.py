# tools.py
import subprocess
from vertexai.generative_models import FunctionDeclaration

# --- TOOL 1: RAG (Context Window Management) ---
def retrieve_relevant_files(issue_description: str):
    """Simulates querying a Vector DB to find relevant files."""
    print(f"Searching codebase for issue: {issue_description}")
    # In production, this would query Vertex AI Vector Search.
    # For this lab, we return a mock file structure.
    return {"file": "auth.py", "content": "def login(user):\n  return True # BUG"}

rag_tool = FunctionDeclaration(
    name="retrieve_relevant_files",
    description="Finds relevant repository files based on the bug report.",
    parameters={"type": "object", "properties": {
        "issue_description": {"type": "string"}
    }}
)

# --- TOOL 2: Code Execution ---
def run_tests():
    """Runs the test suite to verify the fix."""
    result = subprocess.run(['pytest', 'test_auth.py'], capture_output=True, text=True)
    if result.returncode == 0:
        return "SUCCESS: Tests passed."
    return f"FAILURE: {result.stdout}"

test_tool = FunctionDeclaration(
    name="run_tests",
    description="Runs unit tests. Call this after editing code.",
    parameters={"type": "object", "properties": {}}
)


