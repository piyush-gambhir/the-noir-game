import Link from "next/link";
import styles from "./ending.module.css";

type Props = {
  searchParams: Promise<{ type?: string; caught?: string }>;
};

export default async function EndingPage({ searchParams }: Props) {
  const { type, caught } = await searchParams;
  const isConfession = type === "confession";

  const title = isConfession ? "He broke." : "He asked for a lawyer.";
  const sub = isConfession
    ? "Case closed."
    : "He walks. For now.";
  const body = isConfession
    ? "You found the seam. You pressed it. He told you everything — the ledger, the letter opener, the spare key in the storm drain. The recording will go to the DA in the morning."
    : "You pushed too hard, or not in the right places. He invoked. Without his statement, the case sits where it started: a body, a locked study, a missing key, and a man with a smile.";
  const stats =
    isConfession
      ? `Contradictions caught: ${caught || "?"}`
      : `Contradictions caught: ${caught || "?"} — not enough.`;

  return (
    <div className={styles.wrap}>
      <div className={styles.card}>
        <div className={styles.stamp}>
          {isConfession ? "Status — Closed" : "Status — Open"}
        </div>
        <h1 className={styles.title}>{title}</h1>
        <div className={styles.sub}>{sub}</div>
        <div className={styles.divider} />
        <p className={styles.body}>{body}</p>
        <div className={styles.stats}>{stats}</div>
        <div className={styles.actions}>
          <Link href="/" className={styles.btn}>
            Reopen the file
          </Link>
        </div>
      </div>
    </div>
  );
}
