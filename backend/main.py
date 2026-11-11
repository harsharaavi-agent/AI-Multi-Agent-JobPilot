"""FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(title="AI Multi-Agent JobPilot")


@app.get("/health")
def health_check() -> dict:
    """Simple health check endpoint."""
    return {"status": "ok"}
