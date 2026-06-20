"use client";

import { motion, AnimatePresence } from "motion/react";
import type { SuspectState } from "@/lib/signals";
import { SUSPECT_COLOR } from "@/lib/signals";
import styles from "./Transcript.module.css";

export type TranscriptLine = {
  id: string;
  speaker: "detective" | "suspect";
  text: string;
  state?: SuspectState;
  final: boolean;
};

export default function Transcript({ lines }: { lines: TranscriptLine[] }) {
  return (
    <div className={styles.wrap}>
      <AnimatePresence initial={false}>
        {lines.map((line) => {
          const isSuspect = line.speaker === "suspect";
          const color = isSuspect
            ? SUSPECT_COLOR[line.state || "calm"]
            : "var(--detective)";
          const labelColor = isSuspect
            ? SUSPECT_COLOR[line.state || "calm"]
            : "var(--detective-label)";
          const isCracking =
            isSuspect && (line.state === "cracking" || line.state === "breaking");
          return (
            <motion.div
              key={line.id}
              layout
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: line.final ? 1 : 0.55, y: 0 }}
              transition={{ duration: 0.4, ease: "easeOut" }}
              className={styles.line}
            >
              <div className={styles.speaker} style={{ color: labelColor }}>
                {isSuspect ? "Victor Crane" : "Detective"}
              </div>
              <div
                className={styles.text}
                style={{
                  color,
                  fontStyle: isCracking ? "italic" : "normal",
                }}
              >
                {line.text}
              </div>
            </motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
}
