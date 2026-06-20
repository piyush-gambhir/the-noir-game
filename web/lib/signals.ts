/* Frontend mirror of the agent's signal_protocol.py — what we read off
   the suspect participant's attributes after each LLM turn. */

export type SuspectState = "calm" | "defensive" | "cracking" | "breaking";
export type Ending = "confession" | "lawyer_up" | null;

export type SuspectSignal = {
  state: SuspectState;
  stress_level: number;
  contradiction_caught: boolean;
  contradiction_topic: string | null;
  ending: Ending;
  turn_id: string;
  contradictions_caught_count: number;
};

export function readSignal(attrs: Record<string, string>): SuspectSignal {
  return {
    state: (attrs.state as SuspectState) || "calm",
    stress_level: parseFloat(attrs.stress_level || "0"),
    contradiction_caught: attrs.contradiction_caught === "true",
    contradiction_topic: attrs.contradiction_topic || null,
    ending: (attrs.ending as Ending) || null,
    turn_id: attrs.turn_id || "0",
    contradictions_caught_count: parseInt(attrs.contradictions_caught_count || "0", 10),
  };
}

export const SUSPECT_COLOR: Record<SuspectState, string> = {
  calm: "var(--suspect-calm)",
  defensive: "var(--suspect-defensive)",
  cracking: "var(--suspect-cracking)",
  breaking: "var(--suspect-breaking)",
};

export const TOPIC_LABEL: Record<string, string> = {
  alibi_gap: "Alibi gap",
  two_glasses: "The second glass",
  locked_study: "Locked study",
  business_dispute: "Business dispute",
  weapon_familiarity: "Murder weapon",
};
