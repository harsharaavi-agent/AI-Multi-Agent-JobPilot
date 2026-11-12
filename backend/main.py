"""FastAPI application entry point."""

from __future__ import annotations

import os
import secrets
from typing import Any, Dict, List

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from agents.orchestrator import Orchestrator

app = FastAPI(title="AI Multi-Agent JobPilot")


class PrepareApplicationsRequest(BaseModel):
    """Input for scoring jobs and preparing application drafts."""

    resume_text: str = Field(min_length=1, max_length=20000)
    jobs: List[Dict[str, Any]] = Field(min_length=1, max_length=25)


@app.get("/health")
def health_check() -> dict:
    """Simple health check endpoint."""
    return {"status": "ok"}


def verify_api_key(x_api_key: str = Header(default="")) -> None:
    """Protect the workflow endpoint with a deployment-configured API key."""
    expected_api_key = os.getenv("JOBPILOT_API_KEY")
    if not expected_api_key:
        raise HTTPException(
            status_code=503,
            detail="Application preparation is not configured.",
        )
    if not secrets.compare_digest(x_api_key, expected_api_key):
        raise HTTPException(status_code=401, detail="Invalid API key.")


@app.post("/applications/prepare")
def prepare_applications(
    request: PrepareApplicationsRequest,
    _: None = Depends(verify_api_key),
) -> Dict[str, Any]:
    """Return reviewed application drafts without submitting them."""
    return Orchestrator().run(
        {"jobs": request.jobs},
        request.resume_text,
    )
