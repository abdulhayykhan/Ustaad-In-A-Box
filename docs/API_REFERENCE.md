# 🔌 REST API Reference

The **Ustaad-in-a-Box** local backend exposes a lightweight, high-performance REST API built on **FastAPI**. It can be queried by the web UI, external scripts, or mobile devices connected over the local network.

**Base URL:** `http://localhost:8000` (or `http://<HOST_IP>:8000`)  
**Interactive Swagger Docs:** `http://localhost:8000/docs`

---

## 1. Query & Decision Endpoints

### `POST /api/ask`
Submit a text query in English, Urdu script, or Roman Urdu. Runs through the deterministic rule engine and interaction logger.

#### Request Headers
```http
Content-Type: application/json
```

#### Request Body
```json
{
  "text": "battery pholi hui hai"
}
```

#### Response (`200 OK`)
```json
{
  "verdict": "ESCALATE",
  "answer": "Yaar, swollen battery serious cheez hai. Abhi charging band karo aur phone use karna bhi chhoro. Isko mat dabao, mat kholne ki koshish karo. Mujhse milne aao — swollen battery leak ya catch fire kar sakti hai.",
  "rule_id": "BAT-003",
  "rule_label": "Swollen battery",
  "source": "Interview 1, 00:14:22",
  "escalation_reason": "Swollen battery can leak, catch fire, or explode. Stop use immediately.",
  "matched_tags": [
    "battery_swollen"
  ],
  "is_safety_stop": true,
  "all_matched_rules": [
    "BAT-003"
  ],
  "log_id": "a4f8d91c"
}
```

#### Example cURL
```bash
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"screen tooti hai lekin touch chal raha hai\"}"
```

---

### `POST /api/transcribe`
Transcribes incoming audio streams using the CPU-quantized `faster-whisper` model.

#### Request Headers
```http
Content-Type: multipart/form-data
```

#### Form Parameters
| Parameter | Type | Required | Description |
|---|---|---|---|
| `audio` | File (Binary) | Yes | Recorded audio blob (`audio/webm` or `audio/wav`). |

#### Response (`200 OK`)
```json
{
  "transcript": "phone charge nahi ho raha",
  "language": "ur",
  "language_probability": 0.942,
  "confidence": 0.887
}
```

*Note on Low Confidence:* If `confidence < 0.45`, the client web interface prompts the user with the Confirm Step modal before executing.

---

## 2. Auditing & Review Endpoints

### `GET /api/logs`
Returns the historical record of all interactions recorded during the active session.

#### Response (`200 OK`)
```json
[
  {
    "id": "a4f8d91c",
    "ts": "2026-09-29T13:40:48.123456+00:00",
    "input": "battery pholi hui hai",
    "audio_used": false,
    "matched_tags": ["battery_swollen"],
    "rule_id": "BAT-003",
    "rule_label": "Swollen battery",
    "all_matched_rules": ["BAT-003"],
    "verdict": "ESCALATE",
    "is_safety_stop": true,
    "escalation_reason": "Swollen battery can leak, catch fire, or explode. Stop use immediately.",
    "answer": "Yaar, swollen battery serious cheez hai...",
    "review_agree": null,
    "review_disagree": null,
    "review_should_have_escalated": null,
    "review_note": null
  }
]
```

---

### `GET /api/logs/export`
Generates and downloads the technician review worksheet in RFC 4180 CSV format.

#### Response (`200 OK`)
```http
Content-Type: text/csv; charset=utf-8
Content-Disposition: attachment; filename=ustaad_review.csv
```

#### CSV Column Structure
`id`, `ts`, `input`, `verdict`, `rule_id`, `rule_label`, `is_safety_stop`, `escalation_reason`, `review_agree`, `review_disagree`, `review_should_have_escalated`, `review_note`

---

### `GET /api/stats`
Returns aggregated operational metrics for the current session.

#### Response (`200 OK`)
```json
{
  "total": 42,
  "verdicts": {
    "ESCALATE": 18,
    "CAUTION": 16,
    "SAFE": 8
  },
  "safety_stops": 12
}
```

---

## 3. Provenance & System Health Endpoints

### `GET /api/rules`
Dumps all loaded rules currently parsed in memory from `rules.yaml`.

#### Response (`200 OK`)
```json
[
  {
    "id": "BAT-003",
    "label": "Swollen battery",
    "when": ["battery_swollen"],
    "severity": "safety_stop",
    "verdict": "ESCALATE",
    "say": "Yaar, swollen battery serious cheez hai...",
    "escalate": true,
    "reason": "Swollen battery can leak, catch fire, or explode. Stop use immediately.",
    "source": "Interview 1, 00:14:22"
  }
]
```

---

### `GET /api/whisper-status`
Returns the readiness and configuration of the local speech recognition engine.

#### Response (`200 OK`)
```json
{
  "ready": true,
  "model": "base"
}
```
If not ready:
```json
{
  "ready": false,
  "error": "faster-whisper not installed. Run: pip install faster-whisper"
}
```
