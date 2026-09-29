"""
llm.py — Groq LLM Phrasing & Natural Language Layer for Ustaad-in-a-Box

Architectural Rule:
  "Rules decide the verdict; LLM only phrases."
  The deterministic rule engine (engine.py) computes 100% of safety verdicts,
  rule selections, and escalation reasons.
  The Groq LLM layer is strictly used for conversational natural phrasing in
  authentic Karachi Roman Urdu / English, and NEVER overrides safety decisions.
  If Groq is unreachable, offline, or disabled, the system instantly falls back
  to the rule engine's canonical advice.
"""

from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Decision

logger = logging.getLogger("ustaad.llm")


def _load_env_file() -> None:
    """Load key-value pairs from .env into os.environ if not already set."""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        try:
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("\"'")
                    if key and key not in os.environ:
                        os.environ[key] = val
        except Exception as exc:
            logger.warning(f"Failed to read .env file: {exc}")


_load_env_file()


class GroqPhraser:
    """
    Client for Groq's high-speed inference API.
    Rephrases deterministic rule verdicts in Ustaad Bhai's authentic persona.
    """

    DEFAULT_MODEL = "qwen/qwen3.8-27b"
    FALLBACK_MODEL = "openai/gpt-oss-120b"
    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    TRANSCRIPTION_URL = "https://api.groq.com/openai/v1/audio/transcriptions"

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        timeout: float = 4.0,
    ) -> None:
        if api_key is not None:
            self.api_key = api_key.strip()
        else:
            self.api_key = os.environ.get("GROQ_API_KEY", "").strip()
        self.model = model or os.environ.get("GROQ_MODEL", self.DEFAULT_MODEL).strip()
        self.timeout = timeout

    def is_available(self) -> bool:
        """Return True if an API key is configured."""
        return bool(self.api_key and len(self.api_key) > 10)

    def phrase(
        self,
        user_text: str,
        decision: Decision,
        language: str = "auto",
    ) -> tuple[str, str]:
        """
        Rephrase canonical rule advice into Ustaad Bhai's natural conversational voice.
        
        Returns:
            tuple[str, str]: (phrased_text, provider_name)
        """
        # If API key missing, instantly return deterministic rule answer
        if not self.is_available():
            return decision.answer, "deterministic_rule_engine"

        system_prompt = self._build_system_prompt(decision)
        user_prompt = f"Customer Query: {user_text}\nCanonical Rule Advice: {decision.answer}"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.5,
            "max_tokens": 180,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Ustaad-in-a-Box/1.0",
        }

        try:
            req = urllib.request.Request(
                self.API_URL,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                choices = data.get("choices", [])
                if choices:
                    content = choices[0].get("message", {}).get("content", "").strip()
                    if content:
                        return content, f"groq:{self.model}"
        except urllib.error.HTTPError as http_err:
            logger.warning(f"Groq API HTTP Error ({http_err.code}): falling back to rule text")
        except Exception as exc:
            logger.warning(f"Groq API call failed ({exc}): falling back to rule text")

        # Zero-failure fallback: return exact canonical deterministic answer
        return decision.answer, "deterministic_rule_engine"

    def _build_system_prompt(self, decision: Decision) -> str:
        """Construct system instructions enforcing strict alignment with rule verdict."""
        instructions = [
            "You are Ustaad Bhai, a highly experienced, honest electronics repair technician in Karachi.",
            "You run 'Ustaad-in-a-Box', a triage stand-in for smartphone and device triage.",
            "",
            "CRITICAL ARCHITECTURAL CONSTRAINTS:",
            f"1. VERDICT: {decision.verdict} (MUST NOT BE CONTRADICTED).",
            f"2. TRIGGERED RULE: {decision.rule_id} ({decision.rule_label}).",
        ]

        if decision.verdict == "ESCALATE":
            instructions.extend([
                "3. SAFETY ENFORCEMENT: The device is at HAZARD or OUT-OF-RULES risk.",
                "   Firmly tell the customer to stop using, power off, or unplug the device immediately.",
                "   Instruct them to bring it to Ustaad Bhai's shop for bench examination.",
                "   NEVER tell them it is safe or can continue being used.",
            ])
        elif decision.verdict == "CAUTION":
            instructions.extend([
                "3. CAUTION ENFORCEMENT: Explain necessary precautions clearly.",
                "   Highlight warnings without causing undue panic.",
            ])
        else:  # SAFE
            instructions.extend([
                "3. REASSURANCE: Confirm the device is safe for continued use with care.",
            ])

        instructions.extend([
            "",
            "VOICE & PERSONA:",
            "- Speak in warm, authentic, natural Karachi Roman Urdu (or English if the user asked in English).",
            "- Use natural conversational artisan expressions (e.g. 'Bhai', 'Yaar', 'Dekho', 'Fikar na karo').",
            "- Keep response concise (2 to 4 sentences maximum).",
            "- Output ONLY the spoken words. Do not prefix with 'Ustaad Bhai:' or quote marks.",
        ])

        return "\n".join(instructions)

    def transcribe(
        self,
        audio_bytes: bytes,
        filename: str = "audio.webm",
    ) -> Optional[dict]:
        """
        Transcribe audio using Groq's ultra-fast Whisper cloud endpoint.
        Returns dict with keys: transcript, language, confidence, or None on failure.
        """
        if not self.is_available():
            return None

        try:
            import requests

            resp = requests.post(
                self.TRANSCRIPTION_URL,
                headers={"Authorization": f"Bearer {self.api_key}"},
                files={"file": (filename, audio_bytes, "audio/webm")},
                data={
                    "model": "whisper-large-v3-turbo",
                    "response_format": "verbose_json",
                },
                timeout=6.0,
            )
            if resp.status_code == 200:
                data = resp.json()
                text = data.get("text", "").strip()
                lang = data.get("language", "ur")
                segments = data.get("segments", [])
                if segments:
                    avg_logprob = sum(s.get("avg_logprob", -0.3) for s in segments) / len(segments)
                    confidence = max(0.0, min(1.0, 1.0 + avg_logprob))
                else:
                    confidence = 0.95
                return {
                    "transcript": text,
                    "language": lang,
                    "language_probability": 0.95,
                    "confidence": round(confidence, 3),
                    "engine": "groq:whisper-large-v3-turbo",
                }
        except Exception as exc:
            logger.warning(f"Groq transcription failed ({exc}): falling back to local Whisper")

        return None

