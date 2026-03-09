# NB Analytics Service

Portfolio risk scoring API scaffolded via RHDH Golden Path Template.

## Overview

The NB Analytics Service provides real-time portfolio risk scoring for Neuberger Berman's investment management platform.

## Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Liveness/readiness probe |
| `/metrics` | GET | Prometheus metrics |
| `/risk/score` | POST | Score a portfolio |
| `/risk/portfolios` | GET | List portfolios |
| `/risk/portfolios/{id}` | GET | Get portfolio by ID |

## Architecture

- **Runtime:** Python 3.9 / FastAPI
- **Metrics:** Prometheus via prometheus-fastapi-instrumentator
- **Container:** UBI9 Python base image
- **CI:** Tekton Pipelines via Pipelines-as-Code
- **GitOps:** ArgoCD via nb-base-gitops
- **Supply Chain:** RHTAS signing + RHTPA SBOM

## Local Development
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

## API Docs

Swagger UI available at `/docs` when running locally.
