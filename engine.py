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

    # Topics explicitly outside scope — catch them before rule matching.
    OUT_OF_SCOPE_PHRASES: list[str] = [
        "medical", "doctor", "hospital", "dawai", "dawa", "medicine",
        "legal", "lawyer", "police fir", "court", "kanoon", "wakeel",
        "price", "kitna price", "kitne paise", "rate", "quote", "warranty",
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

    def extract_tags(self, text: str) -> list[str]:
        """Return list of matched symptom tags, deduplicated and resolved for conflicts."""
        found: list[str] = []
        for tag, pattern in self._patterns.items():
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
            # Pick first safety stop (they're listed in priority order in YAML)
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
