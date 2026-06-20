"""The Interrogation Room — voice agent (the suspect).

Pipeline: Deepgram STT → Kimi K2.5 (NVIDIA NIM) → ElevenLabs TTS.
Run with:
    python agent.py download-files     # one-time: pull Silero VAD + turn-detector
    python agent.py dev                 # connect to LiveKit Cloud as a worker
"""

from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions, cli, room_io
from livekit.plugins import deepgram, elevenlabs, noise_cancellation, silero
from livekit.plugins import openai as lk_openai
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from signal_protocol import ParsedTurn, attributes_for, parse_turn, voice_settings_for
from suspect import SuspectSession, build_system_prompt

# Load .env from repo root (one dir up)
ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

logger = logging.getLogger("interrogation-room")
logging.basicConfig(level=logging.INFO)

AGENT_NAME = "suspect"  # must match backend's RoomAgentDispatch(agent_name=...)

NVIDIA_NIM_API_KEY = os.environ.get("NVIDIA_NIM_API_KEY", "")
NVIDIA_NIM_BASE_URL = os.environ.get("NVIDIA_NIM_BASE_URL", "https://integrate.api.nvidia.com/v1")
NVIDIA_NIM_MODEL = os.environ.get("NVIDIA_NIM_MODEL", "moonshotai/kimi-k2.5")

ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "")
ELEVENLABS_MODEL = "eleven_flash_v2_5"


async def entrypoint(ctx: JobContext) -> None:
    """One interrogation session."""
    suspect = SuspectSession()

    # ── LLM: Kimi K2.5 via NVIDIA NIM (OpenAI-compatible) ───────────────────
    llm = lk_openai.LLM(
        model=NVIDIA_NIM_MODEL,
        base_url=NVIDIA_NIM_BASE_URL,
        api_key=NVIDIA_NIM_API_KEY,
        temperature=0.85,
    )

    # ── STT: Deepgram nova-3 ────────────────────────────────────────────────
    stt = deepgram.STT(model="nova-3", language="multi")

    # ── TTS: ElevenLabs (voice settings update dynamically per state) ───────
    tts = elevenlabs.TTS(
        voice_id=ELEVENLABS_VOICE_ID,
        model=ELEVENLABS_MODEL,
        voice_settings=elevenlabs.VoiceSettings(**voice_settings_for("calm")),
    )

    session = AgentSession(
        stt=stt,
        llm=llm,
        tts=tts,
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    # ── Hook: intercept LLM output to split structured JSON ─────────────────
    @session.on("conversation_item_added")
    def on_item(ev):
        item = ev.item
        if item.role != "assistant":
            return
        # Schedule async work in the running loop
        asyncio.create_task(_handle_assistant_turn(item, suspect, session, ctx))

    await ctx.connect()

    await session.start(
        room=ctx.room,
        agent=Agent(instructions=build_system_prompt(suspect)),
        room_input_options=room_io.RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Kick off with the suspect's opening line.
    await session.generate_reply(
        instructions=(
            "The detective has just sat down across from you. Greet them briefly "
            "and ask what this is about. Stay calm, slightly cooperative."
        )
    )


async def _handle_assistant_turn(
    item,
    suspect: SuspectSession,
    session: AgentSession,
    ctx: JobContext,
) -> None:
    """Parse JSON, swap voice settings on state change, push attrs to room."""
    raw = item.text_content or ""
    parsed: ParsedTurn = parse_turn(raw)

    suspect.turn_count += 1
    suspect.stress_level = parsed.stress_level
    if parsed.contradiction_topic:
        suspect.contradictions_caught.add(parsed.contradiction_topic)

    # Replace the chat-history text with the spoken-only portion so future
    # LLM context doesn't drift on its own JSON wrapper.
    item.text_content = parsed.speech

    # Voice tone shift on state transition.
    if parsed.state != suspect.current_state:
        new_settings = voice_settings_for(parsed.state)
        try:
            session.tts.update_options(
                voice_settings=elevenlabs.VoiceSettings(**new_settings),
            )
        except Exception as exc:  # plugin may not expose update_options on all versions
            logger.warning("could not update TTS voice_settings live: %s", exc)
        suspect.current_state = parsed.state
        logger.info("state shift: %s (stress %.2f)", parsed.state, parsed.stress_level)

    # Forward to room as participant attributes for the frontend.
    attrs = attributes_for(parsed)
    attrs["turn_id"] = str(suspect.turn_count)
    attrs["contradictions_caught_count"] = str(len(suspect.contradictions_caught))
    try:
        await ctx.room.local_participant.set_attributes(attrs)
    except Exception as exc:
        logger.warning("could not set room attributes: %s", exc)


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, agent_name=AGENT_NAME))
