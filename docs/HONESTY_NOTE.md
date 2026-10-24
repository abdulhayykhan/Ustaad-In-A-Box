# Rocketathon 2026 · Deliverable 03: One-Page Honesty Note (reference version)

**Project:** Ustaad-in-a-Box · **Track:** 1 (Stand-In) · **Team:** DUET

## What it does well
- Safety verdicts come only from `engine.py` and `rules.yaml`. The LLM can reword the answer but cannot change the verdict.
- Hazards (swollen battery, smoke or fire, wet and on, wet and charging, overheating on charger, power bank opened, electric shock) escalate. Unknown or out-of-scope questions escalate as `OUT_OF_RULES` or `OUT_OF_SCOPE` instead of getting a made-up answer.
- Every answer shows the rule ID, tags and source, and every query is logged.
- The core engine and local Whisper work with no internet. The test suite has 64 checks and they pass.

## Where it fails or is unproven
1. **The rules are unverified.** All 20 rules are team-written drafts. No technician has been interviewed or has signed off, and 0 of 20 rows in `ustaad_review.csv` are reviewed. Passing tests only prove the code does what we wrote, not that the advice is right.
2. **Keyword matching is brittle.** It can miss or misread natural speech. Real failures we found and fixed:
   - "swollen battery" missed because of a spelling variant (`phooli`).
   - "touch kaam nahi kar raha" read as touch working.
   - "shock lag raha hai" (electric shock) was matched as a slow phone (`lag`). Fixed with rule `SHK-001`.
   - "wet hai aur charging pe laga diya" and "paani gaya" returned no rule. Fixed.
   - Substring bugs (`fir` in `fire`, `rust` in `frustrated`), fixed with word boundaries.
3. **Known remaining gaps.** Urdu script only covers a few hazard phrases. A phrase like "charging port mein paani gaya" escalates as wet-and-charging even if the phone is not plugged in (over-cautious on purpose). Any wording we did not think of falls to `OUT_OF_RULES`, which is safe but unhelpful.
4. **The LLM guard is coarse.** A text check rejects reassuring wording on an ESCALATE verdict and falls back to the rule text, but it is a keyword check and not proof of safe wording.
5. **Cloud use.** Groq phrasing and transcription are optional and need internet and an API key. Without a key everything falls back to rule text and local Whisper. Live LLM tests only run with a key.
6. **Not benchmarked:** speech accuracy in a noisy hall, latency, power draw, and performance on very old hardware.
7. **Security (booth only):** server on `0.0.0.0` with CORS `*`; `/api/logs` and export have no login. Not for public deployment.

## Why we built it this way
A chatbot that sounds sure of itself is dangerous for battery and water-damage questions. We kept the decision in a small, readable rule list so anyone can see why an answer was given, and made the system say "ask the technician" when it is unsure.

## What we still need
A real technician to review each rule. The review sheet (`ustaad_review.csv`) is ready and empty.
