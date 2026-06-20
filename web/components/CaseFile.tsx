"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { fetchCase, type CaseFile as CaseFileType } from "@/lib/api";
import styles from "./CaseFile.module.css";

function renderInline(text: string) {
  // Render **bold** segments
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((p, i) =>
    p.startsWith("**") && p.endsWith("**") ? (
      <span key={i} className={styles.key}>
        {p.slice(2, -2)}
      </span>
    ) : (
      <span key={i}>{p}</span>
    )
  );
}

export default function CaseFile() {
  const router = useRouter();
  const [data, setData] = useState<CaseFileType | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCase()
      .then(setData)
      .catch((e) => setError(String(e)));
  }, []);

  if (error) {
    return (
      <div className={styles.error}>
        Could not load case file. Is the backend running on http://localhost:8000?
      </div>
    );
  }
  if (!data) {
    return <div className={styles.loading}>Loading file…</div>;
  }

  return (
    <div className={styles.wrap}>
      <div className={styles.file}>
        <div className={styles.stamp}>{data.stamp}</div>
        <h1 className={styles.title}>{data.title}</h1>
        <div className={styles.victim}>{data.victim_line}</div>
        <div className={styles.divider} />

        <div className={styles.body}>
          {data.brief.map((p, i) => (
            <p key={i}>{renderInline(p)}</p>
          ))}

          <div className={styles.sectionLabel}>Known contradictions</div>
          {data.known_contradictions.map((p, i) => (
            <p key={i}>{renderInline(p)}</p>
          ))}

          <div className={styles.sectionLabel}>Your job</div>
          <p>{data.your_job}</p>
        </div>

        <div className={styles.beginArea}>
          <div className={styles.beginHint}>When you're ready</div>
          <button
            className={styles.beginBtn}
            onClick={() => router.push("/room")}
          >
            Begin Interrogation
          </button>
        </div>
      </div>
    </div>
  );
}
