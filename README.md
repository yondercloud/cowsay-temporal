# Cowsay Temporal

A distributed cowsay application built with Temporal workflows, FastAPI, and Docker. This project demonstrates how to use Temporal for orchestrating simple tasks across distributed workers.

## Overview

This application provides a web interface where users can enter messages and receive ASCII art cow responses. The application uses Temporal workflows to distribute cowsay generation tasks to workers, providing reliability and scalability.

## Architecture

- **FastAPI Server** (`server.py`): REST API and web interface
- **Temporal Workflow** (`workflow.py`): Orchestrates cowsay tasks
- **Workers** (`worker.py`): Process cowsay activities
- **Web UI** (`index.html`): Simple frontend for user interaction

## Requirements

- Python 3.11+
- Temporal server running on `localhost:7233` (or configured via `TEMPORAL_HOST`)
- Docker (optional, for containerized deployment)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure Temporal server is running on `localhost:7233`

## Usage

### Running Locally

**Start a worker:**
```bash
python app.py --mode worker
```

**Start the API server:**
```bash
python app.py --mode api
```

The web interface will be available at `http://localhost:8000`

### Docker Usage

**Build the image:**
```bash
make build
```

**Run worker in Docker:**
```bash
make run-worker
```

**Run API server in Docker:**
```bash
make run-api
```

## API Endpoints

- `POST /cowsay` - Generate cowsay output for a message
- `GET /health` - Health check endpoint
- `GET /` - Web interface

## Environment Variables

- `TEMPORAL_HOST` - Temporal server address (default: `localhost:7233`)

## Make Targets

- `make build` - Build Docker image
- `make push` - Push to Docker Hub
- `make run-worker` - Run worker locally in Docker
- `make run-api` - Run API server locally in Docker
- `make restart-api` - Restart deployed API (Kubernetes)
- `make restart-worker` - Restart deployed worker (Kubernetes)

## Development

The application consists of:

- **Workflow** (`workflow.py:16`): `CowsayWorkflow` orchestrates cowsay tasks
- **Activity** (`workflow.py:11`): `say()` function performs the actual cowsay generation
- **API Server** (`server.py:33`): FastAPI endpoint that executes workflows
- **Worker Process**: Connects to Temporal and processes activities

## Deployment

The application is containerized and can be deployed to Kubernetes or any container orchestration platform. The Makefile includes commands for managing deployments.