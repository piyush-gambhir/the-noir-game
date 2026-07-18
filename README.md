# The Interrogation Room

Voice-only noir detective game. You're the detective. The suspect is across the table. Talk your way to a confession before they lawyer up.

## Stack

- **LiveKit Cloud** — real-time audio
- **Deepgram** — speech-to-text
- **Kimi K2.5 via NVIDIA NIM** — the suspect's brain
- **ElevenLabs** — the suspect's voice (with runtime tone shifts)
- **Next.js 16 + React 19** — frontend
- **FastAPI** — token + case server
- **Python LiveKit Agents 1.4+** — the voice pipeline

## Layout

```
the-noir-game/
├── web/              Next.js frontend (TypeScript)
├── backend/          FastAPI token + case server (Python)
├── livekit-agents/   LiveKit voice agent — the suspect (Python)
└── .env.example      Copy to .env and fill in
```

## Setup

```bash
# 1. Copy env file
cp .env.example .env
# Then fill in API keys: LIVEKIT_*, DEEPGRAM_API_KEY, ELEVENLABS_*, NVIDIA_NIM_API_KEY

# 2. Backend
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Agent
cd ../livekit-agents
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python agent.py download-files   # downloads Silero VAD + turn-detector models

# 4. Web
cd ../web
npm install
```

## Run (3 terminals)

```bash
# Terminal 1 — Backend
cd backend && source .venv/bin/activate && uvicorn main:app --reload --port 8000

# Terminal 2 — Agent
cd livekit-agents && source .venv/bin/activate && python agent.py dev

# Terminal 3 — Web
cd web && npm run dev
```

Open http://localhost:3000.

## License

The source code is available under the [MIT License](LICENSE). LiveKit,
Deepgram, NVIDIA NIM, ElevenLabs, and their respective SDKs and services remain
subject to their own terms and licenses.
