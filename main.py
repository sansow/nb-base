"""
NB Analytics Service — Demo API
FastAPI microservice scaffolded via RHDH Golden Path Template
Runs in Coder on OpenShift - Testing pipeline 
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
from typing import Optional
import random
import datetime

app = FastAPI(
    title="NB Analytics Service",
    description="Portfolio risk scoring API — scaffolded via RHDH Golden Path Template",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auto-instrument Prometheus metrics at /metrics
Instrumentator().instrument(app).expose(app)


# ── Models ────────────────────────────────────────────────────────────────────

class Portfolio(BaseModel):
    portfolio_id: str
    assets: list[dict]
    benchmark: Optional[str] = "SP500"


class RiskScore(BaseModel):
    portfolio_id: str
    score: float
    risk_level: str
    var_95: float
    sharpe_ratio: float
    timestamp: str
    model_version: str


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: str


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse, tags=["Ops"])
def health():
    """Liveness/readiness probe — used by OpenShift and ArgoCD health checks."""
    return HealthResponse(
        status="ok",
        service="nb-analytics-svc",
        version="1.0.0",
        timestamp=datetime.datetime.utcnow().isoformat() + "Z",
    )


@app.get("/", tags=["Ops"])
def root():
    return {
        "service": "nb-analytics-svc",
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics",
    }


@app.post("/risk/score", response_model=RiskScore, tags=["Analytics"])
def score_portfolio(portfolio: Portfolio):
    """
    Calculate risk score for a given portfolio.
    
    Returns VaR (95%), Sharpe ratio, and a composite risk score.
    Deployed via RHDH Golden Path Template with RHTAS signing and RHTPA SBOM.
    """
    if not portfolio.assets:
        raise HTTPException(status_code=400, detail="Portfolio must contain at least one asset")

    # Simulated risk calculation (replace with real quant model)
    n = len(portfolio.assets)
    base_score = round(random.uniform(20, 85), 2)
    var_95 = round(random.uniform(1.5, 8.0), 3)
    sharpe = round(random.uniform(0.4, 2.2), 3)

    if base_score < 35:
        risk_level = "LOW"
    elif base_score < 65:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    return RiskScore(
        portfolio_id=portfolio.portfolio_id,
        score=base_score,
        risk_level=risk_level,
        var_95=var_95,
        sharpe_ratio=sharpe,
        timestamp=datetime.datetime.utcnow().isoformat() + "Z",
        model_version="v1.0.0-rhdh",
    )


@app.get("/risk/portfolios", tags=["Analytics"])
def list_portfolios():
    """List sample portfolios (demo data)."""
    return {
        "portfolios": [
            {"id": "NB-EQUITY-001", "name": "NB US Equity Growth", "assets": 42},
            {"id": "NB-FIXED-002",  "name": "NB Fixed Income Core",  "assets": 128},
            {"id": "NB-MULTI-003",  "name": "NB Multi-Asset Alpha",  "assets": 87},
        ]
    }


@app.get("/risk/portfolios/{portfolio_id}", tags=["Analytics"])
def get_portfolio(portfolio_id: str):
    """Get risk summary for a specific portfolio by ID."""
    # Simulated lookup
    portfolios = {
        "NB-EQUITY-001": {"name": "NB US Equity Growth",   "asset_count": 42,  "aum_usd_m": 1240},
        "NB-FIXED-002":  {"name": "NB Fixed Income Core",  "asset_count": 128, "aum_usd_m": 3800},
        "NB-MULTI-003":  {"name": "NB Multi-Asset Alpha",  "asset_count": 87,  "aum_usd_m": 650},
    }
    if portfolio_id not in portfolios:
        raise HTTPException(status_code=404, detail=f"Portfolio {portfolio_id} not found")

    p = portfolios[portfolio_id]
    return {
        **p,
        "portfolio_id": portfolio_id,
        "risk_score": round(random.uniform(30, 70), 2),
        "last_updated": datetime.datetime.utcnow().isoformat() + "Z",
    }
