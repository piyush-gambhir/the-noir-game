"""The Interrogation Room — token + case server.

Two endpoints:
  GET  /api/case               → case file shown to player before interrogation
  POST /api/token              → LiveKit JWT for joining the interrogation room
"""

from __future__ import annotations

import os
import secrets
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from livekit import api
from pydantic import BaseModel

# Load .env from repo root (one dir up from backend/)
ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

LIVEKIT_URL = os.environ.get("LIVEKIT_URL", "")
LIVEKIT_API_KEY = os.environ.get("LIVEKIT_API_KEY", "")
LIVEKIT_API_SECRET = os.environ.get("LIVEKIT_API_SECRET", "")

AGENT_NAME = "suspect"  # must match @server.rtc_session(agent_name=...) in agent.py

app = FastAPI(title="The Interrogation Room")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Case file (v1: Victor Crane) ────────────────────────────────────────────

CASE = {
    "id": "halbrook",
    "title": "The Halbrook Case",
    "stamp": "Homicide Division — File 1184",
    "victim_line": "Margaret Hale — Deceased — November 14th",
    "suspect_name": "Victor Crane",
    "brief": [
        "Margaret Hale, 54, was found dead in the study of her Westfield home at approximately 11:40 PM. Cause of death: a single stab wound. The study was locked from the inside.",
        "Her business partner, **Victor Crane**, 51, was the last known person to see her alive. He claims he left the premises at 10:15 PM to attend a poker game across town.",
    ],
    "known_contradictions": [
        "The poker game host places Crane's arrival at **10:50 PM**. The drive takes **12 minutes**. Crane's alibi has a 23-minute gap.",
        "A glass of scotch was found on Margaret's desk — **two glasses** were used that evening. Crane denies having a drink with her.",
    ],
    "your_job": "Get him talking. Find the cracks. He's careful — but careful people make the most predictable mistakes.",
}


@app.get("/api/case")
async def get_case() -> dict:
    """Return the case file shown to the player before interrogation."""
    return CASE


# ── Token endpoint ──────────────────────────────────────────────────────────


class TokenRequest(BaseModel):
    participant_name: str = "Detective"


class TokenResponse(BaseModel):
    token: str
    livekit_url: str
    room_name: str


@app.post("/api/token", response_model=TokenResponse)
async def create_token(req: TokenRequest) -> TokenResponse:
    if not (LIVEKIT_API_KEY and LIVEKIT_API_SECRET and LIVEKIT_URL):
        raise HTTPException(500, "LiveKit credentials missing — check .env")

    room_name = f"interrogation-{secrets.token_hex(4)}"

    token = (
        api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        .with_identity(req.participant_name)
        .with_name(req.participant_name)
        .with_grants(
            api.VideoGrants(
                room=room_name,
                room_join=True,
                can_publish=True,
                can_subscribe=True,
                can_publish_data=True,
            )
        )
        .with_room_config(
            api.RoomConfiguration(
                agents=[api.RoomAgentDispatch(agent_name=AGENT_NAME)],
            )
        )
        .to_jwt()
    )

    return TokenResponse(token=token, livekit_url=LIVEKIT_URL, room_name=room_name)


@app.get("/api/health")
async def health() -> dict:
    return {"status": "ok"}
