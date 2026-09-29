# 📝 Rocketathon 2026 · Deliverable 03: One-Page Honesty Note

**Project:** Ustaad-in-a-Box  
**Track:** Track 1: Stand-In  
**Team:** Dawood University of Engineering & Technology (DUET)  
**Date:** 29 September 2026  
**Venue:** Expo Centre Karachi  

---

> ### The Guiding Question
> *"Does your system tell the truth about what it is doing, and what it is made of? A system that admits its limits beats a flashier one that hides them."*

---

## 1. Why We Built It This Way: The Architecture of Humility

When tasked with building a "Stand-In" for a human expert, the default temptation is to wrap an LLM in an Urdu system prompt and let it chat. **We rejected this approach intentionally.**

A smartphone customer holding a warm, swelling power bank does not need probabilistic poetry or hallucinated reassurance. They need the exact, unyielding survival rule of a master technician: **"Stop charging immediately. Do not puncture. Power off now."**

We placed 100% of the verdict-rendering authority in a **deterministic, transparent rule engine** (`engine.py`). An AI model is permitted to do speech transcription, but it has **zero authority to declare a hazardous device safe**. If a question does not match an authored rule, the system does not invent an answer: it escalates to the human technician with reason `OUT_OF_RULES`.

---

## 2. Provenance of Rules & Transparent Baseline Status

We explicitly disclose the status of our rule database (`rules.yaml`):
1. **Rule Sourcing:** The 19 authored rules in `rules.yaml` are based on our structured diagnostic questionnaire and common repair heuristics from Saddar mobile market artisans.
2. **Provenance Status:** Every rule is currently labeled with `DRAFT RULE — UNVERIFIED BASELINE (Pending Technician Interview)` in `rules.yaml`. They represent our pre-event operational triage baseline.
3. **Purged Unverified Advice:** Early draft rules included common folk remedies and ungrounded assumptions (such as blanket 2-year battery replacement in `BAT-001`, strict 50% device cost thresholds in `REP-001`, claims of 24h screen blackout in `SCR-003`, or claims that rice starch ruins ports in `WAT-001`/`WAT-002`). During technical review, we purged unverified claims, softened cost heuristics, aligned battery advice with battery health percentage (< 80%) / rapid cycle drops, and clarified that rice is simply ineffective at extracting trapped moisture beneath BGA shielding cans.

---

## 3. The Real Bug Log: What Failed During Bench Testing & How It Was Fixed

Rather than presenting an artificial, spotless score, here is the transparent audit of genuine safety and precision failures discovered and patched during live development:

| # | Bug Observed | Real Input Trigger | Failure Mode | Architectural Root Cause | Remediation Applied |
|---|---|---|---|---|---|
| **1** | **Swollen Battery Missed** | *"Mera phone charge nahi ho raha aur battery phooli hui hai"* | Returned `CAUTION` with port cleaning advice. | Missing stem variants (`"phooli"`, `"phool"`) in `synonyms.yaml`. Only `"pholi"` was present. | Added full phonetic inflection set (`phool`, `phooli`, `phoola`, `phoolna`). Enforced critical safety override whenever hazard tags fire. |
| **2** | **Negation Blind-spot** | *"screen toot gayi touch kaam nahi kar raha"* | Declared `SAFE`! | Input matched both `touch_working` ("touch kaam") and `touch_broken` ("touch kaam nahi"). | Added negation suppression in `engine.py`: if `touch_broken` is present, `touch_working` is forcibly stripped. |
| **3** | **Severity Inversion on Water** | *"Paani mein gira, screen toot gayi, touch kaam kar raha hai"* | Returned `SAFE`! | Specificity sorting prioritized the 2-tag screen rule (`SCR-001`, `normal`) over the 1-tag water rule (`WAT-002`, `caution`). | Inverted sort hierarchy: **Hazard Severity (`caution` > `normal`) strictly dominates specificity**, preventing cosmetic rules from masking hazards. |
| **4** | **Hairdryer Water Short Hazard** | *"Fell in water, dried with hairdryer, now charging"* | Returned `WAT-002` ("Theek kiya ke off hai"). | No compound rule existed for wet devices plugged into AC mains. | Authored `WAT-003` (`severity: safety_stop`, `verdict: ESCALATE`) warning of catastrophic board shorts. |
| **5** | **Substring Collision on "fir"** | *"Phone fire pakad raha hai"* | Treated as `OUT_OF_SCOPE`! | Substring `"fir"` (intended for police FIR) matched inside `"fire"`. | Removed bare `"fir"`, added `"police fir"`, and added strict regex word boundaries (`\b`) to all out-of-scope terms. |
| **6** | **Substring Collision on "rust"** | *"I am frustrated, my phone hangs"* | Fired leaking battery emergency stop! | Substring `"rust"` in `battery_leaking` matched inside `"frustrated"`. | Enforced word boundaries (`\b`) around all synonym dictionary entries. |
| **7** | **Hazard Negations & Price Phrasing** | *"battery leak nahi hui"*, *"kitne ka aayega"* | Fired `BAT-004` on negated leak; price query matched screen rule. | Intrinsic symptom matching lacked clause-aware negation; Roman Urdu price idioms were absent from OOS. | Implemented clause-bounded regex negation window for `NEGATABLE_TAGS` (`battery_swollen`, `battery_leaking`, `overheating`, etc.) and expanded `OUT_OF_SCOPE_PHRASES` with Roman Urdu price queries. |

---

## 4. Current Empirical Verification Status

All 7 probe cases above—alongside 43 standard vernacular queries covering Roman Urdu, Urdu script, and English—are codified as permanent regression tests in `test_engine.py`:

```
============================================================
  Ustaad-in-a-Box — Rule Engine Test Suite
============================================================
  50/50 passed  |  0 failed
============================================================
All unit and adversarial safety tests passed. ✓
```

### Bench Probe Log (`ustaad_review.csv` & `interactions.jsonl`)
The repository includes a live session log of bench probe interactions exported to `ustaad_review.csv`. **We explicitly disclose that the four review columns (`review_agree`, `review_disagree`, `review_should_have_escalated`, `review_note`) are currently empty.** They represent automated bench probes awaiting physical human technician evaluation at our expo booth table, rather than fabricated review scores.

---

## 5. Architectural Trade-offs & Security Disclosures

1. **Unauthenticated Local Network Access:** The backend listens on `0.0.0.0:8000` with CORS `*`. This is an intentional design choice for the hackathon booth: it allows the salvaged phone display to wirelessly stream the UI from the host laptop hotspot without requiring cloud accounts or complex authentication.
2. **Audio Logging Instrumentation:** Early tests showed `audio_used: false` across all rows due to a missing client-side payload flag. We instrumented `AskRequest` and the Web UI so Push-to-Talk vs keyboard inputs are faithfully audited in runtime logs.
3. **Offline Whisper Trade-off:** We use an int8-quantized `faster-whisper` model on local CPU. It has zero cloud latency and 100% offline privacy, but in dense acoustic noise (e.g. loudspeaker announcements), transcription confidence drops. Our **low-confidence Confirm Step modal** (`confidence < 0.45`) was specifically designed to handle this limitation gracefully.

---

## 6. Conclusion

Ustaad-in-a-Box does not pretend to be an omniscient engineer. It is an honest, faithful surrogate for a human craftsman's triage instinct: protecting customers from battery fires, saving salvageable hardware from early landfill disposal, and transparently saying **"I don't know—come see Ustaad Bhai"** when it reaches its limits.
