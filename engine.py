"""
engine.py — Ustaad-in-a-Box Rule Engine

Deterministic rule layer. The LLM (if present) only does phrasing.
This module decides every verdict.

Flow:
  text → extract_tags() → match_rules() → Decision
"""
from __future__ import annotations

import re
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Decision:
    verdict: str                   # SAFE | CAUTION | ESCALATE
    answer: str
    rule_id: Optional[str]
    rule_label: Optional[str]
    source: Optional[str]
    escalation_reason: Optional[str]
    matched_tags: list[str]
    is_safety_stop: bool
    all_matched_rules: list[str]   # all rule IDs that matched, for the why-panel


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class RuleEngine:
    """
    Loads rules.yaml and synonyms.yaml, extracts symptom tags from free text,
    matches them to rules, and returns a Decision.

    Safety-stop rules always take priority.
    No match → OUT_OF_RULES escalation.
    """

    # Tags that by themselves should never produce a SAFE/CAUTION verdict
    # without a matching rule (belt-and-suspenders guard).
    ALWAYS_ESCALATE_TAGS: set[str] = {
        "smoke_smell",
        "battery_swollen",
        "battery_leaking",
    }

    # Hazard tags eligible for contextual negation suppression
    # (e.g. "battery leak nahi hui", "not hot, not swollen").
    # Fault tags with intrinsic negative phrasing (e.g. "charge nahi ho raha") are NOT in this set.
    NEGATABLE_TAGS: set[str] = {
        "battery_swollen",
        "battery_leaking",
        "overheating",
        "water_damage",
        "smoke_smell",
        "device_on",
    }

    # Strict adjacent negation patterns (within 1-2 words). Fails safe:
    ENG_PRE_NEG = re.compile(r"\b(not|no|never)\s+(?:too\s+|very\s+|really\s+)?$", re.IGNORECASE)
    URDU_PRE_NEG = re.compile(r"\b(nahi|nhi|na)\s+(?:koi\s+|bhi\s+|itna\s+|zyada\s+)?$", re.IGNORECASE)
    URDU_POST_NEG = re.compile(
        r"^\s*(?:to|tou|bhi|bilkul)?\s*(?:nahi|nhi)\s*(?:hai|hui|hua|tha|thi)?(?:\s*[,;.\n]|\s*$|\s+(?:lekin|magar|par|aur|and|but)\b)",
        re.IGNORECASE,
    )

    # Topics explicitly outside scope — catch them before rule matching.
    OUT_OF_SCOPE_PHRASES: list[str] = [
        "medical", "doctor", "hospital", "dawai", "dawa", "medicine",
        "legal", "lawyer", "police fir", "court", "kanoon", "wakeel",
        "price", "kitna price", "kitne paise", "kitne ka aayega", "kitne ka",
        "kitnay ka aayega", "kitnay ka", "kitna kharcha", "kitna kharch",
        "kitna lagega", "kitne lagenge", "kitnay lagenge", "kitne ki",
        "kitnay ki", "paise lagenge", "paisay lagenge",
        "repair rate", "kya rate hai", "rate kya hai", "rate batao",
        "service charges", "repair charges", "kitne charges", "kya charges",
        "repair cost", "kitni cost", "cost kitni", "how much does it cost",
        "what is the cost", "how much will it cost", "how much to repair",
        "price quote", "quotation", "cost estimate", "price estimate",
        "warranty",
        "data recovery", "data wapas", "photos wapas", "files wapas",
        "unlock", "unlock karo", "bypass", "frp bypass", "pattern unlock",
        "microwave", "fridge", "refrigerator", "washing machine",
    ]

    def __init__(
        self,
        rules_path: str = "rules.yaml",
        synonyms_path: str = "synonyms.yaml",
    ) -> None:
        base = Path(__file__).parent
        self.rules: list[dict] = self._load_yaml(base / rules_path)
        self.synonyms: dict[str, list[str]] = self._load_yaml(base / synonyms_path)

        # Pre-compile synonym patterns with strict word boundaries
        self._patterns: dict[str, re.Pattern] = {}
        for tag, phrases in self.synonyms.items():
            escaped = []
            for p in phrases:
                p_str = str(p).strip()
                if not p_str:
                    continue
                # Enforce word boundary around all phrases to eliminate substring false-positives
                escaped.append(r"\b" + re.escape(p_str) + r"\b")
            if escaped:
                # Sort longer phrases first so compound matches take precedence
                escaped.sort(key=len, reverse=True)
                pattern = "|".join(escaped)
                self._patterns[tag] = re.compile(pattern, re.IGNORECASE)

        # Pre-compile out-of-scope pattern with strict word boundaries
        escaped_oos = [r"\b" + re.escape(p.strip()) + r"\b" for p in self.OUT_OF_SCOPE_PHRASES if p.strip()]
        escaped_oos.sort(key=len, reverse=True)
        self._oos_pattern = re.compile("|".join(escaped_oos), re.IGNORECASE)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def decide(self, text: str) -> Decision:
        """Entry point: text in → Decision out."""
        text = text.strip()

        # 1. Check out-of-scope first
        if self._is_out_of_scope(text):
            return Decision(
                verdict="ESCALATE",
                answer=(
                    "Yaar, yeh mere scope se bahar hai. Main sirf phones, "
                    "laptops aur power banks ke baare mein baat kar sakta hun. "
                    "Price quotes, warranty, data recovery, ya koi medical/legal "
                    "cheez mere liye nahi hai. Ustaad Bhai se seedha milna behtar hoga."
                ),
                rule_id=None,
                rule_label=None,
                source=None,
                escalation_reason="OUT_OF_SCOPE — topic not covered by this stand-in.",
                matched_tags=[],
                is_safety_stop=False,
                all_matched_rules=[],
            )

        # 2. Extract symptom tags
        tags = self.extract_tags(text)

        # 3. Match rules
        return self.match_rules(tags, text)

    def _is_match_negated(self, text: str, start: int, end: int) -> bool:
        """
        Check if a matched token span is strictly and directly negated.
        Requires direct adjacency (within 1-2 words). Fails safe: when in doubt,
        does not suppress a hazard.
        """
        # 1. Check preceding window (last 2-3 words, max 25 chars)
        pre = text[max(0, start - 25):start]
        clause_split = re.split(r"[,;.\n]|\b(but|lekin|magar|par|aur|and)\b", pre, flags=re.IGNORECASE)
        pre_clause = clause_split[-1] if clause_split else pre
        if self.ENG_PRE_NEG.search(pre_clause) or self.URDU_PRE_NEG.search(pre_clause):
            return True

        # 2. Check directly following window (Roman Urdu trailing negation, e.g. "leak nahi hui")
        # Must not be followed by action verbs like 'chal', 'ho raha', 'on', etc.
        post = text[end:min(len(text), end + 35)]
        if self.URDU_POST_NEG.search(post):
            return True

        return False

    def extract_tags(self, text: str) -> list[str]:
        """Return list of matched symptom tags, deduplicated and resolved for conflicts and negations."""
        found: list[str] = []
        for tag, pattern in self._patterns.items():
            if tag in self.NEGATABLE_TAGS:
                # Find all occurrences; keep tag only if at least one match is NOT negated
                has_unnegated_match = False
                for match in pattern.finditer(text):
                    if not self._is_match_negated(text, match.start(), match.end()):
                        has_unnegated_match = True
                        break
                if has_unnegated_match:
                    found.append(tag)
            else:
                if pattern.search(text):
                    found.append(tag)

        # Conflict & Negation Resolution:
        # If touch is reported broken, suppress touch_working
        if "touch_broken" in found and "touch_working" in found:
            found.remove("touch_working")

        # If touch is working and not broken, infer device is active/on
        if "touch_working" in found and "device_on" not in found:
            found.append("device_on")

        return list(dict.fromkeys(found))  # preserve order, deduplicate

    def match_rules(self, tags: list[str], original_text: str = "") -> Decision:
        """Match tag list against rules. Returns Decision."""
        # Check if an always-escalate hazard appeared anywhere in the raw text
        raw_critical_hazard = False
        for h_tag in self.ALWAYS_ESCALATE_TAGS:
            pat = self._patterns.get(h_tag)
            if pat and pat.search(original_text):
                raw_critical_hazard = True
                break

        if not tags:
            return self._no_match(original_text)

        tag_set = set(tags)

        # Find all rules whose `when` list is a subset of matched tags.
        matched: list[dict] = []
        for rule in self.rules:
            rule_tags = set(rule.get("when", []))
            if rule_tags and rule_tags.issubset(tag_set):
                matched.append(rule)

        # Safety-stop rules take absolute priority
        safety_stops = [r for r in matched if r.get("severity") == "safety_stop"]
        if safety_stops:
            # Prioritize device-specific safety stops (e.g. power_bank, laptop) over generic ones,
            # then more specific condition counts, then YAML order.
            device_tags = {"power_bank", "laptop"}
            safety_stops.sort(
                key=lambda r: (
                    0 if any(t in device_tags for t in r.get("when", [])) else 1,
                    -len(r.get("when", [])),
                )
            )
            rule = safety_stops[0]
            return Decision(
                verdict="ESCALATE",
                answer=rule["say"].strip(),
                rule_id=rule["id"],
                rule_label=rule.get("label", ""),
                source=rule.get("source", ""),
                escalation_reason=rule.get("reason", "Safety rule — escalate to real person."),
                matched_tags=list(tag_set),
                is_safety_stop=True,
                all_matched_rules=[r["id"] for r in matched],
            )

        # Belt-and-suspenders: if any always-escalate hazard tag fired,
        # NEVER return a normal or caution verdict even if a partial rule matched.
        always_esc = tag_set & self.ALWAYS_ESCALATE_TAGS
        if always_esc:
            return Decision(
                verdict="ESCALATE",
                answer=(
                    "Yeh cheez serious hazard hai. Mujhe iska safe jawab nahi pata "
                    "bina Ustaad Bhai ke physical inspection ke — abhi device band karo aur shop le aao."
                ),
                rule_id=None,
                rule_label=None,
                source=None,
                escalation_reason=(
                    f"CRITICAL SAFETY OVERRIDE: Hazard tag matched ({', '.join(always_esc)}) "
                    "prohibits non-escalated verdict."
                ),
                matched_tags=list(tag_set),
                is_safety_stop=True,
                all_matched_rules=[r["id"] for r in matched],
            )

        if not matched:
            return self._no_match(original_text)

        # Non-safety: prioritize severity first (caution > normal) so hazardous issues
        # (like water damage or thermal issues) are NEVER masked by cosmetic 'SAFE' rules,
        # then sort by specificity (more matched conditions), then YAML order.
        severity_order = {"caution": 0, "normal": 1}
        matched.sort(
            key=lambda r: (
                severity_order.get(r.get("severity", "normal"), 99),
                -len(r.get("when", [])),
            )
        )
        rule = matched[0]

        # Critical Safety Invariant: NEVER let a non-hazard/normal rule answer
        # a query that mentions critical battery/smoke hazard terms.
        if raw_critical_hazard and rule.get("severity") == "normal":
            return Decision(
                verdict="ESCALATE",
                answer=(
                    "Aap ki query mein battery/smoke hazard ka zikr hai. "
                    "Kisi bhi risk se bachne ke liye phone ko check karwaye bina normal use na karein — "
                    "Ustaad Bhai ko physical inspection ke liye dikhana zaroori hai."
                ),
                rule_id=None,
                rule_label=None,
                source=None,
                escalation_reason=(
                    "SAFETY OVERRIDE: Query mentions critical hazard terms. "
                    "Prohibiting benign normal verdict."
                ),
                matched_tags=list(tag_set),
                is_safety_stop=True,
                all_matched_rules=[r["id"] for r in matched],
            )

        verdict = rule.get("verdict", "CAUTION")
        return Decision(
            verdict=verdict,
            answer=rule["say"].strip(),
            rule_id=rule["id"],
            rule_label=rule.get("label", ""),
            source=rule.get("source", ""),
            escalation_reason=rule.get("reason") if rule.get("escalate") else None,
            matched_tags=list(tag_set),
            is_safety_stop=False,
            all_matched_rules=[r["id"] for r in matched],
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _is_out_of_scope(self, text: str) -> bool:
        return bool(self._oos_pattern.search(text))

    def _no_match(self, text: str) -> Decision:
        return Decision(
            verdict="ESCALATE",
            answer=(
                "Yeh masla mere samajh mein nahi aaya, ya shayad interview mein "
                "cover nahi hua. Ustaad Bhai se directly poochhna behtar hai — "
                "main galat guidance nahi de sakta."
            ),
            rule_id=None,
            rule_label=None,
            source=None,
            escalation_reason="OUT_OF_RULES — no matching rule found for this symptom combination.",
            matched_tags=[],
            is_safety_stop=False,
            all_matched_rules=[],
        )

    @staticmethod
    def _load_yaml(path: Path) -> any:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def list_rules(self) -> list[dict]:
        """Return all rules (for admin/debug endpoints)."""
        return self.rules
