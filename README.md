# 🔧 Ustaad-in-a-Box

> **A deterministic voice-and-text stand-in for a phone repair technician, built entirely from scrap hardware and free software.**  
> Developed for **Rocketathon 2026** (PK2047 · Expo Centre Karachi) — **Track 1: Stand-In**.

[![Tests](https://img.shields.io/badge/tests-56%2F56%20passed-brightgreen.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)]()
[![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12%20|%203.14-blue.svg)]()
[![Offline](https://img.shields.io/badge/runtime-100%25%20offline-success.svg)]()

---

## 📖 Table of Contents
1. [Core Philosophy & "Why This Idea"](#-core-philosophy--why-this-idea)
2. [How It Works (High-Level Architecture)](#-how-it-works-high-level-architecture)
3. [Repository Structure](#-repository-structure)
4. [Quick Start & Installation](#-quick-start--installation)
5. [The Three Competition Deliverables](#-the-three-competition-deliverables)
6. [Detailed Documentation Suite](#-detailed-documentation-suite)
7. [Rule Engine & Verdict Logic](#-rule-engine--verdict-logic)
8. [Offline Speech & Voice Interface](#-offline-speech--voice-interface)
9. [Evaluation & Honest Failure Reporting](#-evaluation--honest-failure-reporting)
10. [Troubleshooting & FAQ](#-troubleshooting--faq)

---

## 💡 Core Philosophy & "Why This Idea"

### The Competition Challenge
Rocketathon Track 1 asks participants to build a **Stand-In**: *a machine that can hold a real person's place in a room*. The supreme judging question across all tracks is:
> **"Does your system tell the truth about what it is doing, and what it is made of? A system that admits its limits beats a flashier one that hides them."**

### Why a Repair Stand-In Beats Generic Chatbots
Most hackathon teams attempt to build a generic teacher, doctor, or pharmacist clone using an ungrounded large language model (LLM) prompt. This suffers from three fatal flaws:
1. **Hallucination Risk:** Generative LLMs answer confidently even when wrong, which is catastrophic for high-risk advice.
2. **Regulatory & Safety Hazards:** Real-world medical or legal advice violates event rules and poses severe liabilities.
3. **No Grounded Provenance:** A cloud-based LLM lacks connection to a physical craftsman or the event's e-waste ethos.

**Ustaad-in-a-Box is a stand-in architecture for a phone repair technician, running on an authored baseline of unverified draft rules while a formal technician interview and review remain pending.**
- **Tactile, Hard Rules:** A swollen battery means *stop charging immediately*. Water damage with device on means *shut off power now*. Overheating during charging means *unplug*.
- **Deterministic First, Generative Never for Verdicts:** The verdict is computed by strict rule-matching over explicit safety heuristics. An LLM (if enabled) only does language smoothing—it **never** decides whether a device is safe or dangerous.
- **The "Why" Panel:** Every single response displays the exact rule ID triggered, the rule source provenance, and the escalation reason. If no rule matches, it admits ignorance (`OUT_OF_RULES`) rather than guessing.
- **Ties directly into the Scrapyard theme:** The device itself is built from salvaged e-waste and is designed to represent the repair artisan whose trade keeps electronic scrap out of landfills.

---

## 🏗 How It Works (High-Level Architecture)

```
       [User Speech] (Urdu / Roman Urdu / English)
             │
             ▼
    [Push-to-Talk Web UI]
             │ (Audio Blob / WebM)
             ▼
   [Local STT: faster-whisper] ─── (Confidence < 0.45?) ──► [Confirm Step Dialog]
             │                                                ("Kya aap ne yeh kaha?")
             ▼ (Text Transcript)
  ┌─────────────────────────────────────────────────────────────┐
  │                 DETERMINISTIC RULE ENGINE                   │
  │                                                             │
  │  1. Out-of-Scope Filter (pricing, unlocking, medical)      │
  │  2. Regex Synonym Matching (synonyms.yaml)                  │
  │  3. Rule Subset Matching (rules.yaml)                       │
  │  4. Priority Resolution:                                    │
  │     • Safety-Stop Rules (BAT-003, SMK-001, etc.) ──► ESCALATE│
  │     • Caution / Normal Rules                     ──► VERDICT │
  │     • No Match / Out-of-Rules                    ──► ESCALATE│
  └─────────────────────────────────────────────────────────────┘
             │
             ▼
      [Decision Object]
      ├── Verdict: SAFE | CAUTION | ESCALATE
      ├── Answer: Spoken Urdu/Roman Urdu Advice
      ├── Rule ID: (e.g. BAT-003)
      ├── Rule Provenance: (e.g. UNVERIFIED BASELINE)
      └── Matched Symptom Tags: ['battery_swollen']
             │
             ├──────────────────────────┐
             ▼                          ▼
   [Visual UI + Waveform]    [Interaction Logger]
   • Banner with Color/Icon   • Appends to interactions.jsonl
   • "Why" Sidebar Panel      • Computes real-time stats
   • Spoken Voice (Web TTS)   • Generates CSV Review Sheet
```

---

## 📂 Repository Structure

```
Ustaad-In-A-Box/
├── engine.py              # Core deterministic rule engine & tag extractor
├── rules.yaml             # Authored rule definitions with source provenance
├── synonyms.yaml          # Multi-lingual dictionary (Urdu / Roman Urdu / English)
├── logger.py              # JSONL interaction logger & CSV review sheet exporter
├── main.py                # FastAPI backend & audio transcription endpoint
├── test_engine.py         # Automated test suite (56/56 passing)
├── requirements.txt       # Python dependencies (all free & open-source)
├── run.bat                # Windows 1-click startup batch script
│
├── static/
│   └── index.html         # Responsive frontend: PTT mic, waveform, why-panel, TTS
│
├── docs/                  # Detailed documentation suite
│   ├── ARCHITECTURE.md    # Complete system architecture & dataflow
│   ├── BILL_OF_PROVENANCE.md # Rocketathon Deliverable 02 (hardware/software audit)
│   ├── HONESTY_NOTE.md    # Rocketathon Deliverable 03 (failure cases & test review)
│   ├── RULE_AUTHORING_GUIDE.md # Protocol for interviewing & extracting rules
│   ├── API_REFERENCE.md   # Complete REST API schemas & curl examples
│   └── DEMO_SCRIPT.md     # 10-Question Live Pitch script for judges
│
└── interactions.jsonl     # Append-only runtime log of every query & decision
```

---

## 🚀 Quick Start & Installation

### Prerequisites
- **Operating System:** Windows 10/11, Ubuntu 20.04+, or macOS
- **Python:** Python 3.10 to 3.14 (already tested and certified on Python 3.14)
- **Audio Device:** Microphone and speakers (integrated laptop audio or salvaged headset)
- **Internet:** Only needed once during `pip install`; **0% internet required during operation**.

### 1-Click Launch (Windows)
Double-click `run.bat` in the project root:
```cmd
run.bat
```
This script automatically:
1. Installs/verifies dependencies from `requirements.txt`.
2. Executes the full test suite (`test_engine.py`) to verify safety rules.
3. Launches the FastAPI server at `http://localhost:8000`.

### Manual Launch (Cross-Platform)

1. **Clone / Navigate to Directory:**
   ```bash
   cd "C:\Users\USER\OneDrive - Dawood University of Engineering Technology\Desktop\Ustaad-In-A-Box"
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify the Rules:**
   ```bash
   python test_engine.py
   ```

4. **Start the Application:**
   ```bash
   python main.py
   ```
   *Or with Uvicorn directly:*
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

5. **Open in Browser:**
   - **Local Machine:** [http://localhost:8000](http://localhost:8000)
   - **Second Screen / Phone as Face:** Connect your old phone to the same local Wi-Fi or hotspot and open `http://<LAPTOP_LOCAL_IP>:8000`.

---

## 🏆 The Three Competition Deliverables

Rocketathon 2026 mandates three deliverables for submission:

| Deliverable | Description | Where to Find It |
|---|---|---|
| **01. Live Demo** | 10 judge-selected questions handled live via speech/text, correctly answering or escalating with rule IDs shown. | Run `main.py` + see [`docs/DEMO_SCRIPT.md`](docs/DEMO_SCRIPT.md) |
| **02. Bill of Provenance** | Detailed accounting of every scrap component used, previous life, origin, and next destination. | See [`docs/BILL_OF_PROVENANCE.md`](docs/BILL_OF_PROVENANCE.md) |
| **03. One-Page Honesty Note** | Complete disclosure of review scores, failure rates, edge-case limitations, and architectural trade-offs. | See [`docs/HONESTY_NOTE.md`](docs/HONESTY_NOTE.md) |

---

## 📚 Detailed Documentation Suite

For judges, mentors, and developers wanting deep insight into each subsystem:

1. [**System Architecture (`docs/ARCHITECTURE.md`)**](docs/ARCHITECTURE.md)  
   Complete walkthrough of the state machine, decision flowchart, offline speech processing pipeline, and low-latency considerations.
2. [**Bill of Provenance (`docs/BILL_OF_PROVENANCE.md`)**](docs/BILL_OF_PROVENANCE.md)  
   Full audit of physical scrap hardware (laptop, phone, speakers) and free/open-source software licenses.
3. [**Honesty Note & Review Scores (`docs/HONESTY_NOTE.md`)**](docs/HONESTY_NOTE.md)  
   Technical evaluation of the bench evaluation log, bug discoveries, known audio/linguistic failure modes, and safety edge cases.
4. [**Rule Authoring & Interview Protocol (`docs/RULE_AUTHORING_GUIDE.md`)**](docs/RULE_AUTHORING_GUIDE.md)  
   The human capture process: consent form, interview question script, provenance tracking, and YAML authoring.
5. [**REST API Reference (`docs/API_REFERENCE.md`)**](docs/API_REFERENCE.md)  
   Detailed documentation of all JSON endpoints, request/response models, and status codes.
6. [**Judge Demo Script (`docs/DEMO_SCRIPT.md`)**](docs/DEMO_SCRIPT.md)  
   Turn-by-turn script for the 10 live demo questions, demonstration of the confirm step, and answers to hard judge questions.

---

## ⚖️ Rule Engine & Verdict Logic

The rule engine operates deterministically with **zero temperature** and **zero stochastic drift**:

### Severity Levels
1. `safety_stop` (**Immediate Escalation**): Battery swelling, battery punctures/leaks, burning smells, smoke, power bank disassembly, wet devices currently powered on.
2. `caution` (**Action Required**): Fast battery drain, wet phone turned off, broken touch digitizers, laptop thermal throttling, non-charging ports.
3. `normal` (**Informational / Safe**): Superficial screen cracks with working digitizer, basic cache clutter cleaning.

### Match Precedence
```
Input Text
  ├── 1. Check Out-of-Scope (Legal, Medical, Pricing, Unlocking) ──► ESCALATE (OUT_OF_SCOPE)
  ├── 2. Extract Tags from synonyms.yaml
  │      └── If Tag in ALWAYS_ESCALATE_TAGS (e.g. smoke) ───────► ESCALATE
  ├── 3. Match rules.yaml where rule.when ⊆ matched_tags
  │      ├── If any rule is 'safety_stop' ──────────────────────► ESCALATE (Immediate)
  │      ├── Else pick rule with highest severity (caution > normal)
  │      └── Return Rule's Verdict & Captured Phrasing
  └── 4. No Rules Matched ──────────────────────────────────────► ESCALATE (OUT_OF_RULES)
```

---

## 🎙 Offline Speech & Voice Interface

- **Push-to-Talk (PTT):** Bypasses expo hall background noise by only capturing audio while held down.
- **Local STT (`faster-whisper`):** Uses an int8 quantized Whisper model running strictly on local CPU. Requires zero cloud API calls and zero data leaving the device.
- **Audio Fallback:** If speech recognition confidence drops below `0.45` or ambient noise garbles the speech, the system renders an interactive **Confirm Step** dialog (*"Kya aap ne yeh kaha: ...?"*) or invites the user to edit via the typed text box.
- **Text-to-Speech (TTS):** Uses local browser speech synthesis (`SpeechSynthesisUtterance`), preferring Urdu/Hindi voices if installed on the host OS.

---

## 📊 Evaluation & Honest Failure Reporting

Unlike black-box AI prototypes that attempt to fake omniscient capability:
- Every query generates an entry in `interactions.jsonl`.
- Clicking **Download Review CSV** (`/api/logs/export`) outputs a spreadsheet containing:
  - `input`: The exact raw text query.
  - `verdict`: `SAFE`, `CAUTION`, or `ESCALATE`.
  - `rule_id`: The ID of the rule that fired.
  - `review_agree` / `review_disagree` / `review_should_have_escalated`: Review columns to be filled by the real human technician.
- Known failure modes (e.g., compound symptoms with conflicting advice, heavy regional accent STT dropouts) are documented in the [Honesty Note](docs/HONESTY_NOTE.md).

---

## 🛠 Troubleshooting & FAQ

### 1. `faster-whisper` is taking long to load or isn't installed
- **Answer:** The app uses graceful degradation. While Whisper loads (or if it is not installed), the web interface displays `STT: text-only`. You can type in Urdu, Roman Urdu, or English and get instantaneous sub-10ms rule matching.

### 2. Can we run this on a smartphone as a standalone device?
- **Answer:** Yes! The FastAPI backend runs on the salvaged laptop. Connect any smartphone or tablet to the laptop's Wi-Fi hotspot and navigate to `http://<LAPTOP_IP>:8000`. The phone becomes the interactive touch screen, microphone, and speaker "face".

### 3. How do I add or modify a rule?
- **Answer:** Edit `rules.yaml` directly. Add the rule source provenance and your chosen phrasing. Run `python test_engine.py` to ensure all tests pass.

## 👥 Authors & Acknowledgments

- **Team Ustaad-in-a-Box** (Dawood University of Engineering & Technology)
- Built for **Rocketathon 2026** · Powered by **The Rocket Guy Space** × **KYS Alkhidmat Karachi**
- Dedicated to the neighborhood repair technicians who keep Pakistan's electronics running without waste.

---

## 📄 License

This project is open-source software licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

**Rocketathon 2026 · PK2047 · Track 1: Stand-In**  
*Team DUET · Dawood University of Engineering & Technology · Expo Centre Karachi*  
*Powered by The Rocket Guy Space × KYS Alkhidmat Karachi*
