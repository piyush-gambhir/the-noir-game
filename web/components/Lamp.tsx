import styles from "./Lamp.module.css";

export default function Lamp() {
  return (
    <div className={styles.wrap}>
      <div className={styles.cord} />
      <div className={styles.shade} />
      <div className={styles.glow} />
      <div className={styles.tableLine} />
      <div className={styles.tableSurface} />
    </div>
  );
}
