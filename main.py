"""
main.py — Ustaad-in-a-Box FastAPI Server

Endpoints:
  GET  /                    → UI
  POST /api/ask             → text query → Decision JSON
  POST /api/transcribe      → audio file → transcript text
  GET  /api/logs            → all logged interactions
  GET  /api/logs/export     → CSV review sheet download
  GET  /api/stats           → summary counts
  GET  /api/rules           → list all loaded rules (for provenance)

Run:  python main.py
      or: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
"""
from __future__ import annotations

import io
import os
import tempfile
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from engine import RuleEngine
from llm import GroqPhraser
from logger import InteractionLogger

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Ustaad-in-a-Box",
    description="Phone repair technician stand-in. Rules decide the verdict; Groq LLM phrases.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = RuleEngine()
logger = InteractionLogger()
phraser = GroqPhraser()

# ---------------------------------------------------------------------------
# Optional: faster-whisper for local speech-to-text
# ---------------------------------------------------------------------------
_whisper_model = None
_whisper_error: Optional[str] = None

def _load_whisper():
    global _whisper_model, _whisper_error
    try:
        from faster_whisper import WhisperModel
        # Use "base" — fast enough on CPU, decent multilingual quality.
        # Change to "small" for better Urdu accuracy if RAM allows.
        model_size = os.environ.get("WHISPER_MODEL", "base")
        device = "cpu"
        compute = "int8"
        print(f"[whisper] Loading {model_size} on {device}/{compute} …")
        _whisper_model = WhisperModel(model_size, device=device, compute_type=compute)
        print("[whisper] Ready.")
    except ImportError:
        _whisper_error = "faster-whisper not installed. Run: pip install faster-whisper"
        print(f"[whisper] {_whisper_error}")
    except Exception as exc:
        _whisper_error = str(exc)
        print(f"[whisper] Failed to load: {exc}")

# Load Whisper in background so the server starts fast
import threading
threading.Thread(target=_load_whisper, daemon=True).start()

# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class AskRequest(BaseModel):
    text: str
    audio_used: bool = False
    use_llm: bool = True


class AskResponse(BaseModel):
    verdict: str
    answer: str
    rule_id: Optional[str] = None
    rule_label: Optional[str] = None
    source: Optional[str] = None
    escalation_reason: Optional[str] = None
    matched_tags: list[str] = []
    is_safety_stop: bool = False
    all_matched_rules: list[str] = []
    log_id: str
    phrased_by: str = "deterministic_rule_engine"
    canonical_rule_answer: Optional[str] = None


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", include_in_schema=False)
def serve_ui():
    ui_path = Path(__file__).parent / "static" / "index.html"
    return FileResponse(ui_path)


@app.post("/api/ask", response_model=AskResponse)
def ask(body: AskRequest):
    """Submit a text query. Returns verdict, answer, and the rule that fired."""
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="Empty text.")

    decision = engine.decide(body.text.strip())
    canonical_answer = decision.answer
    phrased_by = "deterministic_rule_engine"

    if body.use_llm and phraser.is_available():
        final_answer, phrased_by = phraser.phrase(body.text.strip(), decision)
    else:
        final_answer = canonical_answer

    entry = logger.log(body.text.strip(), decision, audio_used=body.audio_used)

    return AskResponse(
        verdict=decision.verdict,
        answer=final_answer,
        rule_id=decision.rule_id,
        rule_label=decision.rule_label,
        source=decision.source,
        escalation_reason=decision.escalation_reason,
        matched_tags=decision.matched_tags,
        is_safety_stop=decision.is_safety_stop,
        all_matched_rules=decision.all_matched_rules,
        log_id=entry["id"],
        phrased_by=phrased_by,
        canonical_rule_answer=canonical_answer if phrased_by != "deterministic_rule_engine" else None,
    )


@app.post("/api/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    """
    Receive a WebM/WAV audio blob from the browser push-to-talk button.
    Returns { transcript, language, confidence }.
    Uses Groq Whisper-large-v3-turbo if online, falling back to local faster-whisper.
    """
    content = await audio.read()

    # 1. Try Groq Whisper cloud endpoint if available (near-zero latency)
    if phraser.is_available():
        groq_result = phraser.transcribe(content, filename=audio.filename or "audio.webm")
        if groq_result and groq_result.get("transcript"):
            return groq_result

    # 2. Offline fallback: local faster-whisper on CPU
    if _whisper_model is None:
        return {
            "transcript": "",
            "language": "?",
            "confidence": 0.0,
            "error": _whisper_error or "Whisper model still loading — try again in a few seconds.",
        }

    # Write to a temp file (faster-whisper needs a path)
    suffix = ".webm"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # Single-pass transcription with VAD filtering
        seg_generator, info = _whisper_model.transcribe(
            tmp_path,
            beam_size=5,
            language=None,          # auto-detect Urdu / English
            vad_filter=True,        # remove silence
            vad_parameters={"min_silence_duration_ms": 300},
        )
        segments = list(seg_generator)
        text = " ".join(s.text for s in segments).strip()

        # Calculate confidence from avg log-probability of the actual transcribed segments
        avg_logprob = (
            sum(s.avg_logprob for s in segments) / len(segments)
            if segments else -1.0
        )
        confidence = max(0.0, min(1.0, 1.0 + avg_logprob))  # map [-1,0] → [0,1]

        return {
            "transcript": text,
            "language": info.language,
            "language_probability": round(info.language_probability, 3),
            "confidence": round(confidence, 3),
            "engine": "local:faster-whisper",
        }
    except Exception as exc:
        return {"transcript": "", "language": "?", "confidence": 0.0, "error": str(exc)}
    finally:
        Path(tmp_path).unlink(missing_ok=True)


@app.get("/api/llm-status")
def llm_status():
    """Return Groq LLM integration status."""
    return {
        "available": phraser.is_available(),
        "provider": "Groq",
        "model": phraser.model,
        "role": "Conversational phrasing layer (deterministic rule engine retains 100% verdict authority)",
    }


@app.get("/api/logs")
def get_logs():
    """Return all logged interactions."""
    return logger.read_all()


@app.get("/api/logs/export")
def export_logs():
    """Download technician review sheet as CSV."""
    csv_content = logger.export_csv()
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=ustaad_review.csv"},
    )


@app.get("/api/stats")
def stats():
    return logger.stats()


@app.get("/api/rules")
def list_rules():
    """Return all loaded rules (for provenance and debugging)."""
    return engine.list_rules()


@app.get("/api/whisper-status")
def whisper_status():
    if _whisper_model is not None:
        return {"ready": True, "model": os.environ.get("WHISPER_MODEL", "base")}
    return {"ready": False, "error": _whisper_error}


# ---------------------------------------------------------------------------
# Static files (CSS, JS if any)
# ---------------------------------------------------------------------------
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n" + "="*55)
    print("  Ustaad-in-a-Box  v0.1")
    print("  http://localhost:8000")
    print("="*55 + "\n")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,   # set True during development
    )
