"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import {
  useVoiceAssistant,
  RoomAudioRenderer,
  useLocalParticipant,
  useTrackTranscription,
} from "@livekit/components-react";
import { Track } from "livekit-client";
import Lamp from "./Lamp";
import Transcript, { type TranscriptLine } from "./Transcript";
import SpeakingIndicator from "./SpeakingIndicator";
import CrackTag from "./CrackTag";
import { readSignal, type SuspectSignal, type SuspectState } from "@/lib/signals";
import styles from "./InterrogationRoom.module.css";

function fmtElapsed(startMs: number): string {
  const s = Math.floor((Date.now() - startMs) / 1000);
  const m = Math.floor(s / 60);
  const ss = s % 60;
  return `${String(m).padStart(2, "0")}:${String(ss).padStart(2, "0")}`;
}

export default function InterrogationRoom() {
  const router = useRouter();
  const { state, agentTranscriptions, agentAttributes } = useVoiceAssistant();
  const { localParticipant } = useLocalParticipant();

  // Microphone track for the detective's transcription
  const micTrackRef = useMemo(() => {
    const pub = localParticipant?.getTrackPublication(Track.Source.Microphone);
    if (!pub) return undefined;
    return {
      participant: localParticipant,
      publication: pub,
      source: Track.Source.Microphone,
    };
  }, [localParticipant, localParticipant?.audioTrackPublications.size]);

  const { segments: detectiveSegments } = useTrackTranscription(micTrackRef);

  // Decoded suspect signal from agent attributes
  const signal: SuspectSignal = useMemo(
    () => readSignal((agentAttributes as Record<string, string>) || {}),
    [agentAttributes]
  );

  // Track the latest contradiction-caught flag → flash crack tag for 4s
  const [crackVisible, setCrackVisible] = useState(false);
  const [crackTopic, setCrackTopic] = useState<string | null>(null);
  const lastTurnIdRef = useRef<string>("");
  useEffect(() => {
    if (
      signal.contradiction_caught &&
      signal.turn_id !== lastTurnIdRef.current
    ) {
      lastTurnIdRef.current = signal.turn_id;
      setCrackTopic(signal.contradiction_topic);
      setCrackVisible(true);
      const t = setTimeout(() => setCrackVisible(false), 4000);
      return () => clearTimeout(t);
    }
  }, [signal.contradiction_caught, signal.turn_id, signal.contradiction_topic]);

  // Ending → navigate
  useEffect(() => {
    if (signal.ending) {
      const timer = setTimeout(() => {
        router.push(
          `/room/ending?type=${signal.ending}&caught=${signal.contradictions_caught_count}`
        );
      }, 3500); // let the final line finish playing
      return () => clearTimeout(timer);
    }
  }, [signal.ending, signal.contradictions_caught_count, router]);

  // Build the transcript by interleaving detective and suspect segments by timestamp
  const lines = useMemo<TranscriptLine[]>(() => {
    type Seg = { id: string; ts: number; speaker: "detective" | "suspect"; text: string; final: boolean };
    const det: Seg[] = (detectiveSegments || []).map((s) => ({
      id: `d-${s.id}`,
      ts: s.firstReceivedTime ?? 0,
      speaker: "detective",
      text: s.text,
      final: s.final,
    }));
    const sus: Seg[] = (agentTranscriptions || []).map((s) => ({
      id: `s-${s.id}`,
      ts: s.firstReceivedTime ?? 0,
      speaker: "suspect",
      text: s.text,
      final: s.final,
    }));
    const all = [...det, ...sus].sort((a, b) => a.ts - b.ts);
    return all.map((s) => ({
      id: s.id,
      speaker: s.speaker,
      text: s.text,
      final: s.final,
      state: s.speaker === "suspect" ? signal.state : undefined,
    }));
  }, [detectiveSegments, agentTranscriptions, signal.state]);

  // Speaking indicator
  const speaker: "detective" | "suspect" | null =
    state === "speaking"
      ? "suspect"
      : state === "listening" && (localParticipant?.isSpeaking ?? false)
      ? "detective"
      : null;

  // Elapsed time
  const startMsRef = useRef<number>(Date.now());
  const [elapsed, setElapsed] = useState("00:00");
  useEffect(() => {
    const i = setInterval(() => setElapsed(fmtElapsed(startMsRef.current)), 1000);
    return () => clearInterval(i);
  }, []);

  // Connection status messages
  let statusMessage: string | null = null;
  if (state === "connecting") statusMessage = "Connecting…";
  else if (state === "initializing") statusMessage = "He's coming in…";
  else if (state === "disconnected") statusMessage = "Disconnected.";

  return (
    <div className={styles.room}>
      <RoomAudioRenderer />
      <Lamp />
      <SpeakingIndicator
        speaker={speaker}
        suspectState={signal.state as SuspectState}
        elapsed={elapsed}
      />
      <Transcript lines={lines} />
      <CrackTag visible={crackVisible} topic={crackTopic} />
      {statusMessage && <div className={styles.status}>{statusMessage}</div>}
    </div>
  );
}
