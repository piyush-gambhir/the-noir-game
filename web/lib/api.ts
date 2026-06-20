const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export type CaseFile = {
  id: string;
  title: string;
  stamp: string;
  victim_line: string;
  suspect_name: string;
  brief: string[];
  known_contradictions: string[];
  your_job: string;
};

export async function fetchCase(): Promise<CaseFile> {
  const res = await fetch(`${BACKEND}/api/case`, { cache: "no-store" });
  if (!res.ok) throw new Error(`fetchCase failed: ${res.status}`);
  return res.json();
}

export type TokenResponse = {
  token: string;
  livekit_url: string;
  room_name: string;
};

export async function fetchToken(participantName = "Detective"): Promise<TokenResponse> {
  const res = await fetch(`${BACKEND}/api/token`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ participant_name: participantName }),
  });
  if (!res.ok) throw new Error(`fetchToken failed: ${res.status}`);
  return res.json();
}
