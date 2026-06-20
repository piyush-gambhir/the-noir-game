"use client";

import { motion, AnimatePresence } from "motion/react";
import { TOPIC_LABEL } from "@/lib/signals";
import styles from "./CrackTag.module.css";

export default function CrackTag({
  visible,
  topic,
}: {
  visible: boolean;
  topic: string | null;
}) {
  const label = topic ? TOPIC_LABEL[topic] || topic : "Something doesn't add up";

  return (
    <div className={styles.banner}>
      <AnimatePresence>
        {visible && (
          <motion.div
            key="tag"
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 8 }}
            transition={{ duration: 0.4 }}
            className={styles.tag}
          >
            Contradiction caught
          </motion.div>
        )}
      </AnimatePresence>
      <AnimatePresence>
        {visible && (
          <motion.span
            key="desc"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.4, delay: 0.1 }}
            className={styles.desc}
          >
            {label}
          </motion.span>
        )}
      </AnimatePresence>
    </div>
  );
}
