# 🔌 REST API Specification & Reference Guide

The **Ustaad-in-a-Box** local backend exposes a production-grade, lightweight, and high-performance REST API built on **FastAPI** and **Uvicorn**.

It powers the 3D web interface, local diagnostic kiosks, mobile clients on ad-hoc networks, and automated test harnesses.

- **Base URL:** `http://localhost:8000` (or `http://<LAN_IP>:8000`)
- **OpenAPI / Swagger UI:** `http://localhost:8000/docs`
- **ReDoc Interactive UI:** `http://localhost:8000/redoc`

---

## 🧭 Architectural Principles

1. **Deterministic Core Invariant**: `verdict`, `rule_id`, and `is_safety_stop` are computed deterministically by `engine.py`. External LLMs are strictly invoked as text phrasers and cannot alter verdicts.
2. **Offline-First Zero-Latency Fallback**: If an external LLM call fails or times out (>4s), the API immediately returns the deterministic canonical rule text with HTTP 200.
3. **CORS & Zero Authentication**: Open CORS (`allow_origins=["*"]`) and unauthenticated access are intentional architectural choices to allow scrap smartphones, netbooks, and kiosks to interface over local offline Wi-Fi hotspots without requiring SSL or certificate infrastructure.

---

## 📑 Endpoint Summary

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/api/ask` | Submit diagnostic query (Text/Audio input) | None |
| `POST` | `/api/transcribe` | Audio file speech-to-text transcription | None |
| `GET` | `/api/whisper-status` | STT engine readiness and active model | None |
| `GET` | `/api/llm-status` | External Groq LLM availability and active model | None |
| `GET` | `/api/rules` | Complete in-memory rule catalog | None |
| `GET` | `/api/logs` | Active session interaction audit stream | None |
| `GET` | `/api/logs/export` | Download RFC 4180 review worksheet CSV | None |
| `GET` | `/api/stats` | Session aggregate metrics & safety stop counts | None |

---

## 1. Diagnostic Triage Endpoints

### `POST /api/ask`
Processes an incoming device problem description in English, Urdu script, or Roman Urdu through the deterministic triage pipeline and optional Groq conversational phraser.

#### Request Headers
```http
Content-Type: application/json
Accept: application/json
```

#### Request Schema (`AskRequest`)
```json
{
  "text": "string (Required. The symptom description provided by user)",
  "audio_used": "boolean (Optional, default: false. Indicates if source was STT)",
  "use_llm": "boolean (Optional, default: true. If true and Groq is available, rephrases answer)"
}
```

#### Response Schema (`AskResponse` — HTTP 200 OK)
```json
{
  "verdict": "string ('SAFE' | 'CAUTION' | 'ESCALATE')",
  "answer": "string (The final response text spoken/displayed to user)",
  "rule_id": "string | null (e.g. 'BAT-003', or null if out-of-rules)",
  "rule_label": "string | null (Descriptive rule title)",
  "source": "string (Provenance timestamp or draft baseline notice)",
  "escalation_reason": "string | null (Specific hazard rationale)",
  "matched_tags": ["array of strings (Normalized symptom tags extracted)"],
  "is_safety_stop": "boolean (True if physical danger requires immediate power down)",
  "all_matched_rules": ["array of strings (All rule IDs matching query before priority resolution)"],
  "phrased_by": "string | null (e.g. 'groq:qwen/qwen3.8-27b' or null if canonical)",
  "canonical_rule_answer": "string | null (Original deterministic rule text if rephrased)",
  "log_id": "string (Unique 8-character hexadecimal tracking ID)"
}
```

#### Example 1: Physical Hazard (Safety Stop Escalation with Groq Phrasing)
**Request:**
```bash
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"text": "battery phooli hui hai, kya karun?", "use_llm": true}'
```

**Response:**
```json
{
  "verdict": "ESCALATE",
  "answer": "Ustaad bol raha hoon. Bhai, phooli hui battery bohat khatarnaak mamla hai! Sab se pehle phone ko foran charger se hatao aur switch off kar do. Isko dabana ya kholne ki koshish hargiz mat karna, warna aag lag sakti hai ya leak ho sakti hai. Yeh safety ka masla hai, isko dukaan par le aao taake safe tareeqay se handle kiya ja sake.",
  "rule_id": "BAT-003",
  "rule_label": "Swollen battery",
  "source": "DRAFT RULE — UNVERIFIED BASELINE (Pending Technician Interview)",
  "escalation_reason": "Swollen battery can leak, catch fire, or explode. Stop use immediately.",
  "matched_tags": ["battery_swollen"],
  "is_safety_stop": true,
  "all_matched_rules": ["BAT-003"],
  "phrased_by": "groq:qwen/qwen3.8-27b",
  "canonical_rule_answer": "Yaar, swollen battery serious cheez hai. Abhi charging band karo aur phone use karna bhi chhoro. Isko mat dabao, mat kholne ki koshish karo. Mujhse milne aao — swollen battery leak ya catch fire kar sakti hai.",
  "log_id": "936033f3"
}
```

#### Example 2: Out of Scope Query
**Request:**
```bash
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"text": "screen repair kitne rupay ki hogi?"}'
```

**Response:**
```json
{
  "verdict": "ESCALATE",
  "answer": "Price shop par aakar pata chalegi — model aur part availability dekhni parti hai.",
  "rule_id": "OOS-001",
  "rule_label": "Out of scope — price inquiry",
  "source": "DRAFT RULE — UNVERIFIED BASELINE (Pending Technician Interview)",
  "escalation_reason": "Pricing depends on parts, model, and market availability.",
  "matched_tags": ["out_of_scope_price"],
  "is_safety_stop": false,
  "all_matched_rules": ["OOS-001"],
  "phrased_by": null,
  "canonical_rule_answer": null,
  "log_id": "8b22a014"
}
```

---

## 2. Speech & Audio Endpoints

### `POST /api/transcribe`
Ingests an audio recording blob from the client microphone, converting it to text. Implements a dual-engine architecture:
1. Attempts Groq Cloud Whisper (`whisper-large-v3-turbo`) for sub-second recognition.
2. Falls back automatically to local `faster-whisper` on CPU if offline.

#### Request Headers
```http
Content-Type: multipart/form-data
```

#### Form Data Parameters
| Parameter | Type | Required | Description |
|---|---|---|---|
| `audio` | File (Binary) | Yes | Audio file in `audio/webm`, `audio/wav`, `audio/ogg`, or `audio/mp3` format |

#### Response Schema (HTTP 200 OK)
```json
{
  "transcript": "phone pani me gir gaya tha aur ab on nahi ho raha",
  "language": "ur",
  "confidence": 0.895,
  "engine": "groq:whisper-large-v3-turbo"
}
```

#### Fallback Response (When STT unavailable):
```json
{
  "error": "Whisper engine offline or uninitialized",
  "transcript": ""
}
```

---

## 3. Telemetry & Engine Health Endpoints

### `GET /api/llm-status`
Returns real-time status, reachability, and model parameters for the external Groq conversational phraser.

#### Response (HTTP 200 OK)
```json
{
  "available": true,
  "provider": "groq",
  "chat_model": "qwen/qwen3.8-27b",
  "whisper_model": "whisper-large-v3-turbo"
}
```

### `GET /api/whisper-status`
Returns local and cloud STT readiness.

#### Response (HTTP 200 OK)
```json
{
  "ready": true,
  "model": "whisper-large-v3-turbo (cloud) / base (local fallback)"
}
```

### `GET /api/rules`
Dumps the complete catalog of loaded diagnostic rules parsed from `rules.yaml`.

#### Response (HTTP 200 OK)
```json
[
  {
    "id": "BAT-003",
    "label": "Swollen battery",
    "when": ["battery_swollen"],
    "severity": "safety_stop",
    "verdict": "ESCALATE",
    "say": "Yaar, swollen battery serious cheez hai. Abhi charging band karo...",
    "escalate": true,
    "reason": "Swollen battery can leak, catch fire, or explode. Stop use immediately.",
    "source": "DRAFT RULE — UNVERIFIED BASELINE (Pending Technician Interview)"
  }
]
```

### `GET /api/logs`
Returns the append-only JSON audit log of interactions recorded in `interactions.jsonl`.

### `GET /api/logs/export`
Generates and downloads the technician review worksheet in RFC 4180 CSV format.
- Content-Type: `text/csv; charset=utf-8`
- Header: `Content-Disposition: attachment; filename=ustaad_review.csv`

### `GET /api/stats`
Returns aggregated operational metrics for the current session.

#### Response (HTTP 200 OK)
```json
{
  "total": 33,
  "verdicts": {
    "ESCALATE": 14,
    "CAUTION": 12,
    "SAFE": 7
  },
  "safety_stops": 9
}
```

---

## 🐍 Python SDK Integration Example

```python
import requests

BASE_URL = "http://localhost:8000"

def diagnose_symptom(problem_text: str, enable_groq: bool = True):
    payload = {
        "text": problem_text,
        "audio_used": False,
        "use_llm": enable_groq
    }
    
    response = requests.post(f"{BASE_URL}/api/ask", json=payload, timeout=6.0)
    response.raise_for_status()
    data = response.json()
    
    print(f"[{data['verdict']}] (Rule {data['rule_id']})")
    print(f"Safety Stop: {data['is_safety_stop']}")
    print(f"Ustaad Advice: {data['answer']}")
    if data.get('canonical_rule_answer'):
        print(f"Original Rule: {data['canonical_rule_answer']}")
        print(f"Phrased By:    {data['phrased_by']}")
    return data

# Test with a hazardous condition:
diagnose_symptom("phone bohot garam ho gaya aur dhuwan nikal raha hai")
```
