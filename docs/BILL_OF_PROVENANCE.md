# Rocketathon 2026 · Deliverable 02: Bill of Provenance

**Project:** Ustaad-in-a-Box · **Track:** 1 (Stand-In) · **Team:** DUET

This bill lists only what the team can state with confidence. Where the origin or earlier life of a part was not recorded, it says "not recorded" rather than guessing. An incomplete but true bill is better than a detailed one we cannot back up.

## 1. Scrap rule statement

- **Money spent on parts:** not recorded. No purchase receipts exist in this repository, and this document does not claim that nothing was spent.
- **Paid services:** none known. The optional Groq cloud API (chat and transcription) is a third-party service used only if a key is configured. The system runs without it, using the rule engine's own text and local faster-whisper.

## 2. Hardware

| Part | Used for | What it was before | Where it came from | Where it goes after |
|---|---|---|---|---|
| Windows computer used to develop and run the software | Runs the server, rule engine and web interface; displays the interface in a browser | Not recorded | Not recorded | Not recorded |
| The computer's own screen, speaker and microphone (as far as the team can confirm) | Show the interface, speak answers, take push-to-talk input | Part of the computer above | Same as above | Same as above |

No separate salvaged display, speaker, microphone, stand or battery-containment box is claimed. If any were used, they are not documented here, and nothing in this bill should be read as saying they were.

## 3. Software and licences

`requirements.txt` does not pin versions, so exact versions depend on the machine that installed them.

| Package | Purpose | Licence |
|---|---|---|
| Python | Runtime | PSF |
| FastAPI | Local web API | MIT |
| Uvicorn | ASGI server | BSD-3-Clause |
| PyYAML | Reads rules and synonyms | MIT |
| python-multipart | Audio upload parsing | Apache-2.0 |
| requests | Cloud transcription call (optional path) | Apache-2.0 |
| faster-whisper (+ Whisper model weights) | Local offline speech-to-text | MIT (weights: MIT) |
| Browser Web Speech API | Text-to-speech in the browser | Browser feature |
| Own HTML/CSS/JS | Interface | MIT (this repo) |

**Optional cloud services (not scrap, not offline):** Groq chat API and Groq Whisper. Disabled when `GROQ_API_KEY` is empty.

## 4. After the event

No return or recycling plan was recorded for the computer. It is expected to stay with whoever owns it. Nothing was built that needs disposal.
