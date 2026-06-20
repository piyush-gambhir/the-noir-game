"""Game signal protocol — the contract between Kimi's output and the room.

Every LLM turn must emit a JSON object matching `ParsedTurn`. The agent
splits it: `speech` goes to TTS, the rest is forwarded to the frontend
as room participant attributes so the UI can react (transcript color,
crack tag, ending screen, dynamic voice settings).
"""

from __future__ import annotations

import json
import re
from typing import Literal, Optional

from pydantic import BaseModel, Field, ValidationError

State = Literal["calm", "defensive", "cracking", "breaking"]
Ending = Literal["confession", "lawyer_up"]


class ParsedTurn(BaseModel):
    speech: str = Field(..., description="What the suspect says aloud")
    state: State = "calm"
    stress_level: float = Field(0.0, ge=0.0, le=1.0)
    contradiction_caught: bool = False
    contradiction_topic: Optional[str] = None
    ending: Optional[Ending] = None
    internal_note: Optional[str] = None


# ── ElevenLabs voice settings per suspect state ─────────────────────────────
# Lower stability = more emotion / variation. Higher style = more exaggerated.

VOICE_PROFILES: dict[State, dict] = {
    "calm":      {"stability": 0.75, "similarity_boost": 0.85, "style": 0.20, "speed": 1.00, "use_speaker_boost": True},
    "defensive": {"stability": 0.55, "similarity_boost": 0.80, "style": 0.45, "speed": 1.05, "use_speaker_boost": True},
    "cracking":  {"stability": 0.30, "similarity_boost": 0.75, "style": 0.70, "speed": 1.10, "use_speaker_boost": True},
    "breaking":  {"stability": 0.15, "similarity_boost": 0.70, "style": 0.85, "speed": 0.95, "use_speaker_boost": True},
}


def voice_settings_for(state: State) -> dict:
    return VOICE_PROFILES[state]


# ── Parsing ──────────────────────────────────────────────────────────────────

_FENCE_RE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)
_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)


def parse_turn(raw: str) -> ParsedTurn:
    """Parse the LLM output. Tolerant of extra text, code fences, etc.

    Falls back to wrapping the whole thing as plain `speech` if no JSON
    object can be extracted — keeps the game playable even if Kimi
    occasionally drops the schema.
    """
    if not raw or not raw.strip():
        return ParsedTurn(speech="")

    # Try fenced block first
    m = _FENCE_RE.search(raw)
    candidate = m.group(1) if m else None

    # Then any {...} block
    if candidate is None:
        m = _OBJECT_RE.search(raw)
        candidate = m.group(0) if m else None

    if candidate:
        try:
            data = json.loads(candidate)
            return ParsedTurn(**data)
        except (json.JSONDecodeError, ValidationError):
            pass

    # Fallback: treat the whole response as plain speech, calm state.
    return ParsedTurn(speech=raw.strip())


# ── Room attribute forwarding ────────────────────────────────────────────────


def attributes_for(turn: ParsedTurn) -> dict[str, str]:
    """Convert ParsedTurn → string-only attribute dict for LiveKit room."""
    return {
        "state": turn.state,
        "stress_level": f"{turn.stress_level:.2f}",
        "contradiction_caught": "true" if turn.contradiction_caught else "false",
        "contradiction_topic": turn.contradiction_topic or "",
        "ending": turn.ending or "",
        "turn_id": "",  # filled in by caller per-turn
    }
