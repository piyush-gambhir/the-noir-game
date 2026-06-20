"use client";

import type { SuspectState } from "@/lib/signals";
import { SUSPECT_COLOR } from "@/lib/signals";
import styles from "./SpeakingIndicator.module.css";

type Speaker = "detective" | "suspect" | null;

export default function SpeakingIndicator({
  speaker,
  suspectState,
  elapsed,
}: {
  speaker: Speaker;
  suspectState: SuspectState;
  elapsed: string;
}) {
  const color =
    speaker === "suspect" ? SUSPECT_COLOR[suspectState] : "var(--detective)";

  return (
    <div className={styles.bar}>
      <div className={styles.dot} />
      <span>Recording</span>
      <span className={styles.sep}>·</span>
      <span>{elapsed}</span>
      {speaker && (
        <>
          <span className={styles.sep}>·</span>
          <div className={styles.waveform} style={{ color }}>
            {[1, 2, 3, 4, 5].map((i) => (
              <span
                key={i}
                className={styles.bar3}
                style={{
                  animationDelay: `${i * 0.1}s`,
                  height: `${4 + ((i * 7) % 10)}px`,
                  background: "currentColor",
                }}
              />
            ))}
          </div>
          <span style={{ color }}>
            {speaker === "suspect" ? "Victor Crane is speaking" : "You are speaking"}
          </span>
        </>
      )}
    </div>
  );
}
