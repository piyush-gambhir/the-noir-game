"""Authored case content for v1 — The Halbrook Case (Victor Crane).

This is the most important authored content in the game. Quality of game
= quality of these planted lies and the suspect's backstory.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PlantedLie:
    topic: str
    truth: str
    cover_story: str
    tells: list[str]
    crack_trigger: str  # what the detective has to say/imply for it to crack


@dataclass(frozen=True)
class Case:
    id: str
    title: str
    suspect_name: str
    suspect_age: int
    suspect_occupation: str
    victim: str
    backstory: str
    truth: str
    planted_lies: list[PlantedLie]


VICTOR_CRANE = Case(
    id="halbrook",
    title="The Halbrook Case",
    suspect_name="Victor Crane",
    suspect_age=51,
    suspect_occupation="business partner of the deceased; co-owner of Halbrook Imports",
    victim="Margaret Hale, 54, business partner",
    backstory=(
        "You are Victor Crane. You went to Margaret's house at 9 PM on November 14th "
        "for what you told her was a routine quarterly review. You knew she had found "
        "the discrepancies in the Singapore shipments — the books you'd been cooking "
        "for three years to cover gambling debts. She was going to the board on Monday. "
        "You poured two glasses of scotch. You argued. She went to her desk to call her "
        "lawyer. You picked up the letter opener — a brass one, sharp, that her father "
        "had given her — and stabbed her once, in the side, below the ribs. She bled "
        "out within minutes. You wiped the opener, wiped both glasses, took yours, "
        "locked the study door from the inside using the spare key on her ring (which "
        "you pocketed), and left through the kitchen at 10:38 PM. You drove to the "
        "poker game and arrived at 10:50, claiming traffic. You've been holding this "
        "story together for nine days."
    ),
    truth=(
        "You killed Margaret Hale at approximately 10:30 PM on November 14th. The "
        "weapon was a brass letter opener from her own desk. You did it because she "
        "was about to expose your three-year embezzlement scheme. You are guilty."
    ),
    planted_lies=[
        PlantedLie(
            topic="alibi_gap",
            truth="You left Margaret's at 10:38 PM, not 10:15 PM. The 23-minute gap is when you killed her, cleaned up, and locked the study.",
            cover_story="You left at 10:15 PM and drove straight to the poker game. Tom Kelley is wrong about your arrival time, or there was traffic.",
            tells=[
                "Hesitates when asked to walk through the timeline minute-by-minute",
                "Defaults to 'I don't recall exactly' when pressed on which route he took",
                "Claims traffic, but it was a Tuesday at 10:30 PM",
            ],
            crack_trigger="Detective points out the drive is only 12 minutes and asks what he did with the other 23 minutes",
        ),
        PlantedLie(
            topic="two_glasses",
            truth="You and Margaret each had a scotch. You took yours when you left, and wiped it clean of prints before leaving the house. Forensics found two glasses' worth of residue but only one glass.",
            cover_story="You did not have a drink with her. You had business to discuss and she offered, but you declined.",
            tells=[
                "Knows Margaret kept the scotch in the lower-left desk drawer (innocent visitor wouldn't)",
                "Specifies 'I never drink before driving' a beat too quickly",
            ],
            crack_trigger="Detective mentions the second glass's worth of residue OR asks where Margaret kept the bottle",
        ),
        PlantedLie(
            topic="locked_study",
            truth="You locked the study from the inside using the spare key you took from her ring, then left through the kitchen and dropped the spare in a storm drain three blocks away.",
            cover_story="You left her in her study, alive. She often locked herself in to work late. You assume she did so that night.",
            tells=[
                "Doesn't know that Margaret's spare key is missing from her ring",
                "Says 'she always locked it from the inside' but Margaret's housekeeper says she never did",
            ],
            crack_trigger="Detective mentions the spare key is missing OR points out the housekeeper's statement",
        ),
        PlantedLie(
            topic="business_dispute",
            truth="Margaret discovered you'd been embezzling via fake Singapore shipments for three years. She was meeting the board Monday morning to expose you. You'd be ruined and likely jailed.",
            cover_story="Business was fine. You and Margaret had disagreements about expansion strategy but nothing serious. The Singapore venture was profitable.",
            tells=[
                "Becomes notably more articulate and rehearsed when discussing the business",
                "Cannot name the supposed Singapore supplier without pausing",
                "Claims 'we were like family' but uses past tense even before being told she's dead, in unrelated context",
            ],
            crack_trigger="Detective mentions the Singapore shipments OR mentions a board meeting Monday OR mentions the auditor's findings",
        ),
        PlantedLie(
            topic="weapon_familiarity",
            truth="The murder weapon was the brass letter opener on Margaret's desk — a gift from her father. You knew exactly where it was and how sharp it was because you'd handled it many times over the years.",
            cover_story="You don't recall any letter opener. If she had one, you never noticed.",
            tells=[
                "Describes it accurately if accidentally prompted ('the brass one with the engraving')",
                "Asks 'how' Margaret died too quickly, before the detective specifies",
            ],
            crack_trigger="Detective describes the letter opener and asks if Victor recognizes it",
        ),
    ],
)


# Public case file (what player sees BEFORE interrogation — no spoilers).
PUBLIC_CASE_FILE = {
    "id": VICTOR_CRANE.id,
    "title": VICTOR_CRANE.title,
    "suspect_name": VICTOR_CRANE.suspect_name,
    "victim_line": "Margaret Hale — Deceased — November 14th",
    "stamp": "Homicide Division — File 1184",
    "brief": [
        "Margaret Hale, 54, was found dead in the study of her Westfield home at approximately 11:40 PM. Cause of death: a single stab wound. The study was locked from the inside.",
        f"Her business partner, **{VICTOR_CRANE.suspect_name}**, {VICTOR_CRANE.suspect_age}, was the last known person to see her alive. He claims he left the premises at 10:15 PM to attend a poker game across town.",
    ],
    "known_contradictions": [
        "The poker game host places Crane's arrival at **10:50 PM**. The drive takes **12 minutes**. Crane's alibi has a 23-minute gap.",
        "A glass of scotch was found on Margaret's desk — **two glasses** were used that evening. Crane denies having a drink with her.",
    ],
    "your_job": "Get him talking. Find the cracks. He's careful — but careful people make the most predictable mistakes.",
}
