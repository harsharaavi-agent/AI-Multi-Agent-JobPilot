# AI Multi-Agent JobPilot

A lightweight multi-agent job application assistant built with Python.

## Structure

- `agents/` contains the orchestration and job/resume matching logic.
- `backend/` includes the FastAPI API entry point.
- `database/` holds model and mock persistence layers.
- `tools/` contains utilities like job retrieval, resume parsing, and email generation.
- `prompts/` stores prompt templates for matching and resume tailoring.
- `tests/` includes the basic pytest suite.

## Getting started

1. Create a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `pytest`
4. Start the API: `uvicorn backend.main:app --reload`

## Notes

This project is scaffolded for extension with real job search providers, resume parsing libraries, and LLM-powered matching logic.
