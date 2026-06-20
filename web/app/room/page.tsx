"use client";

import { useEffect, useState } from "react";
import { LiveKitRoom } from "@livekit/components-react";
import InterrogationRoom from "@/components/InterrogationRoom";
import { fetchToken } from "@/lib/api";

export default function RoomPage() {
  const [conn, setConn] = useState<{ token: string; url: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchToken("Detective")
      .then((r) => setConn({ token: r.token, url: r.livekit_url }))
      .catch((e) => setError(String(e)));
  }, []);

  if (error) {
    return (
      <div
        style={{
          minHeight: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontFamily: "var(--font-sans)",
          fontSize: 13,
          opacity: 0.6,
          padding: 20,
          textAlign: "center",
        }}
      >
        Could not get a session token. Is the backend running on http://localhost:8000?
      </div>
    );
  }

  if (!conn) {
    return (
      <div
        style={{
          minHeight: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontFamily: "var(--font-sans)",
          fontSize: 11,
          letterSpacing: "0.15em",
          textTransform: "uppercase",
          opacity: 0.5,
        }}
      >
        Entering the room…
      </div>
    );
  }

  return (
    <LiveKitRoom
      token={conn.token}
      serverUrl={conn.url}
      connect
      audio
      video={false}
    >
      <InterrogationRoom />
    </LiveKitRoom>
  );
}
