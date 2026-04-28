#!/usr/bin/env python3
"""
TCS Wings Backend - Standalone deployment package
Deploy to: https://render.com (free tier) or Railway

For Render deployment:
1. Create account at render.com
2. Create Web Service
3. Connect GitHub repo or upload this folder
4. Set start command: gunicorn app.main:app --bind 0.0.0.0:$PORT

Environment variables needed:
- DATABASE_URL: your PostgreSQL connection string (or use SQLite locally)
"""

import os

# Ensure we're in the backend directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)