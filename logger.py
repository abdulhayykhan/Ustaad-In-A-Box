"""
logger.py — Interaction logger for Ustaad-in-a-Box

Logs every query/decision to a JSONL file and exports a CSV review sheet
for the technician to mark agree / disagree / should_have_escalated.
"""
from __future__ import annotations

import csv
import io
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from engine import Decision


class InteractionLogger:
    def __init__(self, log_path: str = "interactions.jsonl") -> None:
        self.path = Path(log_path)

    def log(self, input_text: str, decision: Decision, audio_used: bool = False) -> dict:
        """Write one interaction to the JSONL log. Returns the entry."""
        entry = {
            "id": str(uuid.uuid4())[:8],
            "ts": datetime.now(timezone.utc).isoformat(),
            "input": input_text,
            "audio_used": audio_used,
            "matched_tags": decision.matched_tags,
            "rule_id": decision.rule_id,
            "rule_label": decision.rule_label,
            "all_matched_rules": decision.all_matched_rules,
            "verdict": decision.verdict,
            "is_safety_stop": decision.is_safety_stop,
            "escalation_reason": decision.escalation_reason,
            "answer": decision.answer,
            # Review fields — filled in by technician offline
            "review_agree": None,
            "review_disagree": None,
            "review_should_have_escalated": None,
            "review_note": None,
        }
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return entry

    def read_all(self) -> list[dict]:
        if not self.path.exists():
            return []
        entries = []
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        return entries

    def export_csv(self) -> str:
        """Return CSV string for technician review sheet."""
        entries = self.read_all()
        output = io.StringIO()
        fieldnames = [
            "id", "ts", "input", "verdict", "rule_id", "rule_label",
            "is_safety_stop", "escalation_reason",
            "review_agree", "review_disagree", "review_should_have_escalated",
            "review_note",
        ]
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for entry in entries:
            writer.writerow(entry)
        return output.getvalue()

    def stats(self) -> dict:
        entries = self.read_all()
        total = len(entries)
        if total == 0:
            return {"total": 0}
        verdicts = {}
        safety_stops = 0
        for e in entries:
            v = e.get("verdict", "?")
            verdicts[v] = verdicts.get(v, 0) + 1
            if e.get("is_safety_stop"):
                safety_stops += 1
        return {
            "total": total,
            "verdicts": verdicts,
            "safety_stops": safety_stops,
        }
