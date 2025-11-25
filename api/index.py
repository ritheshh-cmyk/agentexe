import os
import sys

# Add the current directory to sys.path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from server.main import app
except Exception as e:
    # Fallback app to show startup errors
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    import traceback
    
    app = FastAPI()
    
    @app.get("/{catchall:path}")
    def catch_all(catchall: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Application failed to start",
                "detail": str(e),
                "traceback": traceback.format_exc()
            }
        )

# Vercel ASGI handler
handler = app
