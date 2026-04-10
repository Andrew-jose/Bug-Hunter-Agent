# Bug Hunter AI Agent

# 🤖 Bug Hunter AI Agent

An autonomous, serverless AI agent that identifies, fixes, and tests software bugs using Google Gemini and FastAPI, deployed on Google Cloud Run.

**[Link to Live Demo]** | **[Link to Architecture Diagram]**

## 🚀 Overview
The Bug Hunter Agent is designed to streamline the debugging pipeline. Instead of developers manually tracing errors, this system ingests bug reports, searches the codebase using RAG (Retrieval-Augmented Generation), writes the patch, and runs tests autonomously. 

Crucially, it implements a **Human-in-the-Loop (HITL)** architecture, ensuring no code is merged without final developer approval.

## 📸 See it in Action
*[Pro-Tip: Upload the screenshot you took earlier of the green success messages and embed it here!]*
![Agent UI Screenshot](link-to-your-image.png)

## 🏗️ Architecture & Tech Stack
* **Frontend:** Streamlit (Python)
* **Backend API:** FastAPI
* **AI Engine:** Google Gemini Pro (via Google AI Studio)
* **Deployment:** Google Cloud Run (Serverless Docker Container)
* **Key Patterns:** Retrieval-Augmented Generation (RAG), Multi-Agent Workflow, Human-in-the-Loop (HITL).

## ✨ Core Features
1. **Autonomous RAG Workflow:** The agent searches the repository for the exact file causing the issue.
2. **Self-Correction Loop:** It writes the fix and runs a simulated test. If it fails, the agent refactors its own code before proceeding.
3. **Safety Gate (HITL):** Suspends the workflow and awaits an HTTP POST request from a human manager before initiating a mock Git merge.
4. **Cloud-Native:** Completely serverless backend utilizing environment variables for secure port binding and API key management.

## 💻 How to Run Locally

1. Clone the repository:
   ```bash
   git clone [https://github.com/Andrew-jose/Bug-Hunter-Agent.git](https://github.com/Andrew-jose/Bug-Hunter-Agent.git)
   cd Bug-Hunter-Agent
