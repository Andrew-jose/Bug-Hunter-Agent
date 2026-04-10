#!/usr/bin/env python3
"""
Local development server with environment variable loading.
Use this instead of running main.py directly.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Verify required environment variables
required_vars = ['GCP_PROJECT_ID']
missing_vars = [var for var in required_vars if not os.environ.get(var)]

if missing_vars:
    print("❌ ERROR: Missing required environment variables:")
    for var in missing_vars:
        print(f"   - {var}")
    print("\n📝 Please create a .env file based on .env.example")
    exit(1)

print("✅ Environment variables loaded successfully")
print(f"📍 GCP Project: {os.environ.get('GCP_PROJECT_ID')}")
print(f"🌍 GCP Location: {os.environ.get('GCP_LOCATION', 'us-central1')}")
print(f"🔌 Port: {os.environ.get('PORT', '8080')}\n")

# Import and run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    from main import app
    
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
