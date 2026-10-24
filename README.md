# 🔧 Ustaad-in-a-Box: Hardware Diagnostic Stand-In

> **An offline-resilient, voice-and-text diagnostic kiosk that serves as an exact procedural stand-in for a veteran phone repair technician.**  
> Built from **salvaged e-waste hardware** and **free open-source software**, featuring a **deterministic safety rule engine**, a **3D animated spatial web interface**, and an optional **Groq Cloud LLM** conversational phrasing layer.

Developed for **Rocketathon 2026** (PK2047 · Expo Centre Karachi) · **Track 1: Stand-In**.

---

<p align="center">
  <img src="https://img.shields.io/badge/Engine%20Tests-64%20Passing-brightgreen?style=for-the-badge&logo=pytest" alt="Rule Tests" />
  <img src="https://img.shields.io/badge/LLM%20Tests-need%20API%20key-yellow?style=for-the-badge&logo=openai" alt="LLM Tests" />
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="MIT License" />
  <img src="https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12%20|%203.14-informational?style=for-the-badge&logo=python" alt="Python Versions" />
  <img src="https://img.shields.io/badge/Frontend-Vanilla%20HTML5%20%2F%203D%20CSS3-orange?style=for-the-badge&logo=html5" alt="3D Frontend" />
  <img src="https://img.shields.io/badge/Core%20features-work%20offline-success?style=for-the-badge" alt="Core features work offline" />
  <img src="https://img.shields.io/badge/Hardware-see%20Bill%20of%20Provenance-blueviolet?style=for-the-badge" alt="Scrap Cost" />
</p>

---

## 📑 Master Table of Contents

1. [Executive Summary & The Stand-In Challenge](#-executive-summary--the-stand-in-challenge)
2. [Why a Repair Stand-In Beats Generic Chatbots](#-why-a-repair-stand-in-beats-generic-chatbots)
3. [The Core Architectural Invariant: Rules Decide, LLM Only Phrases](#-the-core-architectural-invariant-rules-decide-llm-only-phrases)
4. [3D Animated Spatial Web Interface](#-3d-animated-spatial-web-interface)
5. [End-to-End System Block Diagram](#-end-to-end-system-block-diagram)
6. [Complete Diagnostic Rule Catalog (Taxonomy)](#-complete-diagnostic-rule-catalog-taxonomy)
7. [Clause-Scoped Negation & Hazard Protection](#-clause-scoped-negation--hazard-protection)
8. [Dual-Engine Audio & Speech-to-Text Pipeline](#-dual-engine-audio--speech-to-text-pipeline)
9. [Physical Hardware Salvage & E-Waste Build](#-physical-hardware-salvage--e-waste-build)
10. [Repository Directory Structure](#-repository-directory-structure)
11. [Quick Start & Setup Instructions](#-quick-start--setup-instructions)
12. [REST API Specification Overview](#-rest-api-specification-overview)
13. [Verification & Automated Test Matrix](#-verification--automated-test-matrix)
14. [Rocketathon Competition Deliverables Alignment](#-rocketathon-competition-deliverables-alignment)
15. [Documentation Suite Sitemap](#-documentation-suite-sitemap)
16. [Contributing & Code of Conduct](#-contributing--code-of-conduct)
17. [License & Acknowledgments](#-license--acknowledgments)

---

## 💡 Executive Summary & The Stand-In Challenge

In the informal electronics markets of Karachi (Regal Chowk, Saddar, Shershah), neighborhood phone repair artisans (*Ustaads*) are the frontline guardians against electronic waste and household hazards. When a phone battery starts bulging, or liquid spills into a charging port, a customer needs an authoritative answer to one vital safety question before mishandling the device:

> **"Is this device safe to keep using, and what should I do next?"**

Under **Rocketathon 2026 Track 1 (Stand-In)**, the challenge is to build a machine that **holds a real person's place in a room**. The supreme judging standard across all tracks is:

> *"Does your system tell the truth about what it is doing, and what it is made of? A system that admits its limits beats a flashier one that hides them."*

**Ustaad-in-a-Box** answers this call. It is not an unconstrained AI pretending to be an all-knowing bot. It is an honest, deterministic procedural stand-in for a veteran phone repair technician. It operates on verified physical safety heuristics, admits when a question falls outside its rule catalog (`OUT_OF_RULES`), and halts immediately on catastrophic physical hazards.

---

## 🥊 Why a Repair Stand-In Beats Generic Chatbots

Most hackathon teams attempt to clone a generic schoolteacher, lawyer, or medical doctor using raw LLM system prompts. This strategy fails in mission-critical environments:

| Failure Mode | Generic Generative Chatbot | Ustaad-in-a-Box Stand-In |
|---|---|---|
| **Hallucination Risk** | Confidently invents dangerous DIY battery punctures or hair-dryer advice. | **Verdicts come only from the rule engine (the LLM only rephrases text)**. Verdicts are locked to formal YAML rules. |
| **Safety Criticality** | Softly suggests troubleshooting while a lithium pouch undergoes thermal runaway. | **Hard Safety Stop**. Immediately outputs `ESCALATE` and orders power disconnection. |
| **Auditable Provenance** | Black box neural weights; impossible to trace why an answer was generated. | **Full rule provenance**. Every response displays rule ID, tags, source tape counter, and why it fired. |
| **Offline Operation** | Requires high-bandwidth multi-billion-parameter cloud APIs. | **Works offline** (rule engine + local Whisper); cloud phrasing/transcription is optional. Target hardware: an old laptop; not benchmarked on a Core 2 Duo. |
| **Ethical Scope** | Attempts to diagnose human illnesses or give financial speculation. | **Strict Out-of-Scope Shield**. Rejects non-repair questions (`OOS-001`). |

---

## 🏛️ The Core Architectural Invariant: Rules Decide, LLM Only Phrases

The system implements a rigid dual-engine separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. DETERMINISTIC RULE ENGINE (engine.py)                   │
│    - Evaluates input symptoms against synonyms.yaml         │
│    - Enforces clause-scoped negation boundaries             │
│    - Computes Verdict: SAFE | CAUTION | ESCALATE            │
│    - Enforces Safety-Stop Supremacy                         │
│    - Selects Rule ID (e.g. BAT-003) & Canonical Advice      │
└──────────────────────────────┬──────────────────────────────┘
                               │
            [ Rigid Decision Contract & Rule Constraints ]
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. OPTIONAL GROQ CLOUD PHRASER (llm.py)                    │
│    - Model: qwen/qwen3-32b (latency not benchmarked)              │
│    - Persona: Authentic Karachi Repair Artisan (Ustaad)     │
│    - Dialect: Natural Roman Urdu & Colloquial English       │
│    - STRICT GUARD: Cannot alter verdict or dilute hazards   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. PRESENTATION & AUDIT TELEMETRY                           │
│    - Displays Verdict Plaque + Phrased Advice               │
│    - Expandable [🔍 View Canonical Deterministic Rule Text] │
│    - Instant Zero-Downtime Fallback if Groq is Offline      │
└─────────────────────────────────────────────────────────────┘
```

1. **Deterministic Authority**: The rule engine has unilateral power over safety verdicts. If `engine.py` decides `ESCALATE`, no LLM prompt can downgrade it to `SAFE`.
2. **Dialect Grounding**: The LLM serves solely to vocalize technical guidance in the warm, authentic phrasing of a Karachi electronics craftsman (*"Bhai jaan, swollen battery serious cheez hai..."*).
3. **Dual-Engine Toggle**: The user can flip the `⚡ Groq LLM` switch in the header to alternate between the LLM rephrased output and the raw canonical deterministic rule text.

---

## 🎨 3D Animated Spatial Web Interface

Built entirely in **vanilla HTML5, CSS3 3D transforms, and minimal JavaScript** (zero external frameworks, no Three.js, zero CDN bloat):

- **Perspective Matrix Floor**: A CSS3 perspective plane (`perspective: 550px rotateX(68deg)`) rendering an infinite glowing cybernetic workbench grid.
- **3D Holographic Gyroscope**: Dual concentric gimbal rings orbiting on separate 3D axes (`rotateX(68deg)` and `rotateY(60deg)`) around the technician core.
- **Real-Time Cursor Micro-Parallax**: A lightweight (<20 lines) `requestAnimationFrame` interpolation loop that tilts the holographic avatar in 3D space (`rotateY` / `rotateX`) as the user navigates the screen.
- **Machined 3D Push-To-Talk Button**: A tactile hardware button featuring multi-stop radial gradients, a recessed bevel socket, and physical depress mechanics (`translateZ(3px) translateY(7px)`).
- **3D Glassmorphism Cards**: Cards utilize `backdrop-filter: blur(16px)` and enter with 3D flip-in perspective transitions (`perspective(1000px) rotateX(16deg)` → `rotateX(0deg)`).
- **Pulsing 3D Safety Strobe**: A glowing crimson hazard beacon (`⚠ SAFETY STOP`) pops out with physical depth (`translateZ(12px)`) when immediate danger is detected.

---

## 🔄 End-to-End System Block Diagram

```mermaid
flowchart TD
    subgraph Client ["Client Presentation Layer (Vanilla HTML5 / 3D CSS3 / Minimal JS)"]
        UI_Input["User Input\n(Push-to-Talk Mic / Keyboard)"]
        Avatar_3D["3D Hologram Gyroscope\n(Perspective Core + Micro-Parallax)"]
        Waveform["Oscilloscope Waveform\n(HTML5 2D Canvas)"]
        Verdict_Plaque["3D Verdict Plaque\n(SAFE / CAUTION / ESCALATE)"]
        Canonical_Box["Inspection Drawer\n(Canonical Rule Advice)"]
        Why_Sidebar["Telemetry 'Why' Panel\n(Rule ID, Tags, Provenance)"]
        TTS_Speaker["Web Speech Synthesis\n(Urdu/Regional Voices)"]
    end

    subgraph Backend ["FastAPI Application Backend (Localhost:8000)"]
        API_Gateway["FastAPI Gateway\n(/api/ask, /api/transcribe)"]
        
        subgraph Audio_Pipeline ["Audio Processing Subsystem"]
            STT_Router{"Transcription Router"}
            Groq_STT["Groq Cloud Whisper\n(whisper-large-v3-turbo)"]
            Local_STT["faster-whisper Engine\n(CPU int8 Quantized, VAD Filter)"]
        end

        subgraph Core_Engine ["Deterministic Rule Core (engine.py)"]
            OOS_Gate["Stage 1: Out-of-Scope Filter\n(Regex Lexicon: Medical/Legal/Price)"]
            Tag_Extractor["Stage 2: Vernacular Tag Extractor\n(synonyms.yaml + Word Boundaries)"]
            Negation_Analyzer["Stage 3: Clause-Scoped Negation\n(Prevents Hazard Erasure)"]
            Rule_Matcher["Stage 4: Rule Set Inclusion\n(rules.yaml Set Intersections)"]
            Precedence_Engine["Stage 5: Precedence & Safety-Stop\n(Safety Stops > Caution > Safe)"]
        end

        subgraph Phrasing_Layer ["Dual-Engine Phraser (llm.py)"]
            Groq_Check{"Groq API Enabled?"}
            Groq_Model["Groq Qwen3 32B Phraser (optional)\n(Karachi Artisan Persona)"]
            Raw_Rule["Canonical Baseline Text\n(Pre-compiled Expert Guidance)"]
        end

        subgraph Persistence ["Persistence & Auditing"]
            JSONL_Log["interactions.jsonl\n(Append-Only Audit Stream)"]
            CSV_Sheet["Review Sheet Generator\n(/api/logs/export)"]
        end
    end

    %% Wiring
    UI_Input -- "Audio Blob (WebM)" --> API_Gateway
    UI_Input -- "Text Query" --> API_Gateway
    API_Gateway --> STT_Router
    STT_Router -->|Cloud Available| Groq_STT
    STT_Router -->|Offline Fallback| Local_STT
    Groq_STT --> OOS_Gate
    Local_STT --> OOS_Gate
    API_Gateway --> OOS_Gate

    OOS_Gate --> Tag_Extractor
    Tag_Extractor --> Negation_Analyzer
    Negation_Analyzer --> Rule_Matcher
    Rule_Matcher --> Precedence_Engine

    Precedence_Engine --> Groq_Check
    Groq_Check -->|Yes| Groq_Model
    Groq_Check -->|No / Offline| Raw_Rule

    Groq_Model --> JSONL_Log
    Raw_Rule --> JSONL_Log
    JSONL_Log --> CSV_Sheet

    Groq_Model --> API_Gateway
    Raw_Rule --> API_Gateway

    API_Gateway --> Verdict_Plaque
    API_Gateway --> Canonical_Box
    API_Gateway --> Why_Sidebar
    API_Gateway --> Avatar_3D
    API_Gateway --> TTS_Speaker
    API_Gateway --> Waveform
```

---

## 📋 Complete Diagnostic Rule Catalog (Taxonomy)

The baseline diagnostic knowledge is encoded in [`rules.yaml`](rules.yaml) and organized across standard categories:

| Rule ID | Severity | Verdict | Trigger (`when`) | Description |
|---|---|---|---|---|
| `BAT-003` | `safety_stop` | **ESCALATE** | `['battery_swollen']` | Swollen battery |
| `BAT-004` | `safety_stop` | **ESCALATE** | `['battery_leaking']` | Leaking or dented battery |
| `SMK-001` | `safety_stop` | **ESCALATE** | `['smoke_smell']` | Smoke or burning smell |
| `WAT-001` | `safety_stop` | **ESCALATE** | `['water_damage', 'device_on']` | Water damage — device currently on |
| `WAT-002` | `caution` | **CAUTION** | `['water_damage']` | Water damage — device already off |
| `WAT-003` | `safety_stop` | **ESCALATE** | `['water_damage', 'charging']` | Water damage — connected to charger |
| `CHG-002` | `safety_stop` | **ESCALATE** | `['overheating', 'charging']` | Overheating while charging |
| `PWR-001` | `safety_stop` | **ESCALATE** | `['power_bank', 'opening_device']` | Power bank fault or opening |
| `PWR-002` | `safety_stop` | **ESCALATE** | `['power_bank', 'overheating']` | Power bank overheating / charging hazard |
| `CHG-001` | `normal` | **CAUTION** | `['charging_fault']` | Device not charging |
| `BAT-001` | `normal` | **CAUTION** | `['battery_drain']` | Fast battery drain |
| `SCR-000` | `normal` | **CAUTION** | `['cracked_screen']` | Cracked screen — general inquiry |
| `SCR-001` | `normal` | **SAFE** | `['cracked_screen', 'touch_working']` | Cracked screen — touch working |
| `SCR-002` | `caution` | **CAUTION** | `['cracked_screen', 'touch_broken']` | Cracked screen — touch not working |
| `SCR-003` | `caution` | **CAUTION** | `['screen_ink_bleed']` | Screen internal damage — purple ink / lines / bleeding |
| `DEV-001` | `normal` | **CAUTION** | `['slow_device']` | Slow or hanging device |
| `DEV-002` | `caution` | **CAUTION** | `['overheating']` | Phone overheating — general |
| `LAP-001` | `caution` | **CAUTION** | `['laptop', 'overheating']` | Laptop overheating |
| `REP-001` | `normal` | **CAUTION** | `['repair_vs_replace']` | Repair vs replace |
| `SHK-001` | `safety_stop` | **ESCALATE** | `['electric_shock']` | Electric shock from device or charger |

*Plus out-of-scope (price, unlock, medical/legal, other appliances) and `OUT_OF_RULES` fallbacks, which always escalate. Every rule is an unverified draft; see the Honesty Note.*

---

## 🛡️ Clause-Scoped Negation & Hazard Protection

Natural spoken Urdu frequently includes negative words (*"nahi"*, *"not"*, *"never"*, *"no"*). Naive keyword systems suffer from **Hazard Concealment**:

```text
User Input: "phone charge nahi ho raha aur battery phool gayi hai"
```

A naive parser sees *"nahi"*, concludes the sentence is negated, drops both tags, and marks the device `SAFE`. **This would cause a user to continue carrying an exploding battery!**

### Our Multi-Layered Protection Solution:
1. **Clause Splitting**: The query is split across conjunction boundaries (`aur`, `lekin`, `par`, `but`, `,`, `.`).
2. **Clause-Scoped Negation Scope**: The word *"nahi"* only neutralizes tags residing in its immediate sub-clause (`"phone charge nahi ho raha"` neutralizes `charging_fault`).
3. **Hazard Tag Asymmetry**: Severe hazards (`battery_swollen`, `battery_leaking`, `smoke_smell`) require explicit syntactic binding to a negative modifier (e.g. *"battery phooli nahi hai"*) before they can be dropped.
4. **Regression Test Verification**: Dedicated probe tests in `test_engine.py` verify that composite sentences like *"swollen + not charging"* correctly escalate to `BAT-003`.

---

## 🎙️ Dual-Engine Audio & Speech-to-Text Pipeline

In an exhibition hall with 80dB background noise, generic continuous listening fails. Our pipeline applies four layers of acoustic resilience:

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Judge
    participant UI as 3D Web UI
    participant Audio as Audio Router
    participant Groq as Groq Whisper (Cloud)
    participant Local as faster-whisper (CPU int8)
    participant Engine as Rule Engine

    User->>UI: Hold Push-to-Talk (🎙️)
    UI->>UI: Stream Audio WebM Buffer
    User->>UI: Release Push-to-Talk
    UI->>Audio: POST /api/transcribe
    
    alt Groq Online (typically fast; not benchmarked)
        Audio->>Groq: Transcribe WebM Blob
        Groq-->>Audio: Return Transcript + High Confidence
    else Groq Offline / Timeout
        Audio->>Local: Process int8 CPU Transcription + VAD
        Local-->>Audio: Return Local Transcript
    end

    alt Confidence < 0.45
        Audio-->>UI: Low Confidence Warning
        UI->>User: Display Confirm Step ("Kya aap ne yeh kaha: ...?")
        User->>UI: Click "✓ Haan, yahi"
    end

    UI->>Engine: POST /api/ask { text }
    Engine-->>UI: Return Verdict & Spoken Advice
    UI->>User: Render 3D Banner & Vocalize Web Speech
```

- **Push-to-Talk (PTT)**: Captures audio *only* when held down, eliminating ambient hall noise between queries.
- **Voice Activity Detection (VAD)**: Strips leading and trailing dead air before passing to speech models.
- **Multilingual Recognition**: Roman Urdu and English are covered by the rules; Urdu script has only a handful of hazard phrases (swollen, smoke, water, shock) and otherwise falls back to `OUT_OF_RULES`.
- **Confirm Step Fallback**: If confidence drops below `0.45`, the system renders a confirmation prompt (*"Kya aap ne yeh kaha: '[Transcript]'?"*) allowing the user to verify before execution.

---

## 🔩 Physical Hardware

The physical stand is built from salvaged parts. The authoritative, team-confirmed list (what each part was, where it came from, where it goes after) is in [`docs/BILL_OF_PROVENANCE.md`](docs/BILL_OF_PROVENANCE.md); build notes are in [`docs/HARDWARE_SALVAGE_SPEC.md`](docs/HARDWARE_SALVAGE_SPEC.md). This README deliberately does not repeat part lists, so the documents cannot disagree.

---

## 📂 Repository Directory Structure

```
Ustaad-In-A-Box/
├── engine.py                   # Core deterministic rule engine & tag extractor
├── llm.py                      # Groq LLM natural phrasing & cloud Whisper layer
├── rules.yaml                  # 20 authored DRAFT rules with provenance sources
├── synonyms.yaml               # Multi-lingual dictionary (Urdu / Roman Urdu / English)
├── logger.py                   # Append-only interaction logger & CSV review generator
├── main.py                     # FastAPI application server & API routes
├── test_engine.py              # Deterministic rule test suite (64 checks)
├── test_llm.py                 # External Groq LLM integration test suite (offline guard test + 3 live tests that need a Groq key)
├── package_submission.py       # Automated submission packaging script
├── requirements.txt            # Python dependencies (free & open source)
├── run.bat                     # Windows 1-click launch batch script
├── .env.example                # Configuration template for Groq API keys
├── LICENSE                     # MIT License
├── CONTRIBUTING.md             # Developer contribution & rule authoring guide
│
├── static/
│   └── index.html              # 3D spatial UI (Vanilla HTML5 / 3D CSS3 / Minimal JS)
│
├── docs/                       # Exhaustive documentation suite
│   ├── ARCHITECTURE.md         # Comprehensive system architecture & dataflow
│   ├── BILL_OF_PROVENANCE.md   # Rocketathon Deliverable 02 (Hardware/Software audit)
│   ├── HONESTY_NOTE.md         # Rocketathon Deliverable 03 (Failure cases & review log)
│   ├── RULE_AUTHORING_GUIDE.md # Protocol for interviewing technicians & authoring YAML
│   ├── API_REFERENCE.md        # Comprehensive REST API reference with OpenAPI schemas
│   ├── DEPLOYMENT_GUIDE.md     # Production deployment on scrap laptops & Raspberry Pi
│   ├── HARDWARE_SALVAGE_SPEC.md# E-waste bill of materials & battery safety chamber
│   ├── DEMO_SCRIPT.md          # 10-Question live demonstration pitch script
│   └── SUBMISSION_CHECKLIST.md # Pre-flight validation checklist for judges
│
├── interactions.jsonl          # Immutable runtime audit log of all interactions
├── ustaad_review.csv           # RFC 4180 export worksheet for human-in-the-loop review
```

---

## 🚀 Quick Start & Setup Instructions

### System Requirements
- **OS**: Windows 10/11, Debian/Ubuntu Linux, Raspberry Pi OS, or macOS.
- **Python**: Python 3.10 to 3.14 (Python 3.10+; test suite run on the versions listed in the Honesty Note).
- **Network**: Internet connection required *only* during initial `pip install` or if using Groq Cloud API. **Core features work offline**; Groq phrasing/transcription are optional extras that need internet.

### 1-Click Launch (Windows)
Double-click [`run.bat`](run.bat) in the project directory. The batch script verifies dependencies, runs unit tests, and launches the server.

### Manual Setup (Cross-Platform)

```bash
# 1. Clone the repository
git clone https://github.com/abdulhayykhan/Ustaad-In-A-Box.git
cd Ustaad-In-A-Box

# 2. Create and activate a virtual environment
python -m venv venv
# Linux / macOS:
source venv/bin/activate
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment (Optional: add your Groq API key)
cp .env.example .env

# 5. Run the automated test suites
python test_engine.py
python test_llm.py

# 6. Start the server
python main.py
```

Open your browser to: **`http://localhost:8000`**

---

## 🔌 REST API Specification Overview

The local FastAPI backend serves the frontend and external kiosks over clean REST endpoints:

| Endpoint | Method | Description | Primary Payload / Parameters |
|---|---|---|---|
| `/api/ask` | `POST` | Execute triage on text query | `{"text": "...", "audio_used": false, "use_llm": true}` |
| `/api/transcribe` | `POST` | Transcribe speech audio blob | `multipart/form-data` with `audio` file blob |
| `/api/whisper-status`| `GET` | Check local & cloud STT readiness | Returns `{ "ready": true, "model": "..." }` |
| `/api/llm-status` | `GET` | Check Groq API health & model | Returns `{ "available": true, "chat_model": "..." }` |
| `/api/rules` | `GET` | Dump in-memory rule catalog | Returns array of loaded rules from `rules.yaml` |
| `/api/logs` | `GET` | Audit stream of session queries | Returns array of interaction objects |
| `/api/logs/export`| `GET` | Download review sheet CSV | Downloads `ustaad_review.csv` |
| `/api/stats` | `GET` | Real-time session metrics | Returns counts for `ESCALATE`, `CAUTION`, `SAFE` |

*For complete request schemas, response codes, and Python SDK code samples, see [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md).*

---

## 🧪 Verification & Automated Test Matrix

Quality assurance is maintained through continuous regression testing:

```
test_engine.py : 64 checks, all passing (run: python test_engine.py)
test_llm.py    : 1 offline guard test always runs; 3 live tests are SKIPPED
                 unless GROQ_API_KEY is set and the network is reachable.
```
*Passing tests show the listed cases behave as written. They do not show the rules are correct: no technician has reviewed them yet.*

---

## 🏆 Rocketathon Competition Deliverables Alignment

| Deliverable | Requirement | How Ustaad-in-a-Box Satisfies It |
|---|---|---|
| **Deliverable 01: Live Demo** | 10 live questions answered with rule IDs, audible speech, and correct escalation. | Follow the turn-by-turn judge walkthrough in [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md). |
| **Deliverable 02: Bill of Provenance** | Full audit of scrap hardware, previous lives, origin, software licenses, and destination. | Comprehensive accounting in [`docs/BILL_OF_PROVENANCE.md`](docs/BILL_OF_PROVENANCE.md). |
| **Deliverable 03: Honesty Note** | Transparent disclosure of failures, accuracy limitations, and design trade-offs. | Unfiltered engineering post-mortem in [`docs/HONESTY_NOTE.md`](docs/HONESTY_NOTE.md). |

---

## 📚 Documentation Suite Sitemap

| Document | Purpose & Contents |
|---|---|
| 🏛️ [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Exhaustive architecture, dataflow diagrams, and state machines |
| 🔌 [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md) | Full REST API documentation with cURL & Python SDK examples |
| 🎙️ [`docs/RULE_AUTHORING_GUIDE.md`](docs/RULE_AUTHORING_GUIDE.md) | Technician consent form, interview script, and YAML schemas |
| 🐧 [`docs/DEPLOYMENT_GUIDE.md`](docs/DEPLOYMENT_GUIDE.md) | Scrap laptop, Raspberry Pi, systemd, and kiosk setup instructions |
| 🔩 [`docs/HARDWARE_SALVAGE_SPEC.md`](docs/HARDWARE_SALVAGE_SPEC.md)| E-waste Bill of Materials & battery safety quarantine enclosure |
| 📜 [`docs/BILL_OF_PROVENANCE.md`](docs/BILL_OF_PROVENANCE.md) | Full audit of scrap materials and open-source software packages |
| 🔍 [`docs/HONESTY_NOTE.md`](docs/HONESTY_NOTE.md) | Open disclosure of edge cases, bug discoveries, and failure modes |
| 🎭 [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md) | Turn-by-turn 10-Question demonstration script for competition judges |
| 📋 [`docs/SUBMISSION_CHECKLIST.md`](docs/SUBMISSION_CHECKLIST.md) | Pre-flight submission validation and judge checklist |

---

## 🤝 Contributing & Code of Conduct

We welcome contributions from electronics repair technicians, right-to-repair advocates, and software engineers. Please review [`CONTRIBUTING.md`](CONTRIBUTING.md) for our contribution workflow, test-driven development requirements, and ethics guidelines.

---

## 📄 License & Acknowledgments

- **License**: Released under the terms of the open-source [MIT License](LICENSE).
- **Developers**: Abdul Hayy Khan & Contributors (Dawood University of Engineering & Technology, Karachi).
- **Event**: Built for **Rocketathon 2026** (PK2047, Karachi) · Powered by **The Rocket Guy Space** × **KYS Alkhidmat Karachi**.
- **Special Tribute**: Dedicated to the neighborhood repair technicians of Saddar and Regal Chowk, whose daily ingenuity keeps Pakistan's electronics working and out of landfills.
