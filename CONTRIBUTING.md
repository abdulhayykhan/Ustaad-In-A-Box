# Contributing to Ustaad-in-a-Box

Thank you for your interest in contributing to **Ustaad-in-a-Box**!

Ustaad-in-a-Box was engineered for **Rocketathon 2026 (PK2047, Karachi)** under **Track 1: Stand-In**. The project is dedicated to public safety, electronics right-to-repair, and ethical AI engineering built on salvaged hardware.

Before contributing, please read this document carefully to understand our strict safety constraints, architecture boundaries, and verification mandates.

---

## 🧭 Core Architectural Invariant: "Rules Decide; LLM Only Phrases"

Every contributor must understand the foundational design contract of this project:

> **The deterministic rule engine (`engine.py`) has 100% unilateral authority over diagnostic verdicts, rule selections, and escalation reasons.**
> 
> The Large Language Model (Groq / Qwen / Llama) is strictly an auxiliary styling and dialect phraser. Under no circumstances may an LLM decide whether a device is `SAFE`, `CAUTION`, or `ESCALATE`.

If an incoming pull request introduces non-deterministic model inference into the safety decision path, it will be closed immediately.

---

## 🛡️ Code of Conduct & Safety Philosophy

1. **Safety First**: Lithium-ion battery swelling, thermal runaway, internal electrical shorts, and water immersion with high-voltage charging are physical fire and explosion hazards. We never downplay risk to sound optimistic.
2. **Honesty Over Perfection**: We do not fabricate benchmark scores or fake interview timestamps. Unverified rules must be labeled `DRAFT RULE — UNVERIFIED BASELINE`. Real bugs must be documented openly in [`docs/HONESTY_NOTE.md`](docs/HONESTY_NOTE.md).
3. **Salvage & Accessibility**: The front-end must remain pure vanilla HTML5, CSS3, and minimal vanilla JavaScript. No React, no Vite build steps, no heavy Node.js runtimes, and no external CDN dependencies that prevent 100% offline operation on salvaged Core 2 Duo laptops.

---

## 🚀 How to Set Up Your Development Environment

### 1. Prerequisites
- Python 3.10+ (tested through Python 3.14).
- Git.
- Optional: A free Groq Cloud API key from [console.groq.com](https://console.groq.com) for cloud phrasing and cloud Whisper STT.

### 2. Clone the Repository
```bash
git clone https://github.com/abdulhayykhan/Ustaad-In-A-Box.git
cd Ustaad-In-A-Box
```

### 3. Virtual Environment & Dependencies
```bash
python -m venv venv

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Linux / macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env and supply your GROQ_API_KEY (optional, fallback engine works offline)
```

### 5. Run the Test Suites
```bash
python test_engine.py
python test_llm.py
```
All 60+ tests must pass before you start writing code.

---

## 📋 Rule Authoring & Modification Workflow

Every diagnostic rule lives in [`rules.yaml`](rules.yaml), and linguistic variations live in [`synonyms.yaml`](synonyms.yaml).

### Step 1: Rule Schema Requirements
Every entry in `rules.yaml` must follow this exact schema:

```yaml
- id: "XXX-000"                      # Category prefix + 3 digits (e.g. BAT-005)
  label: "Human readable summary"    # Short descriptive title
  severity: "escalate" | "caution" | "safe"
  safety_stop: true | false          # Mandatory TRUE if physical hazard
  when:                              # List of tag identifiers
    - "primary_symptom"
    - "secondary_condition"
  precedence: 100                    # Integer (higher number = higher priority)
  source: "DRAFT RULE — UNVERIFIED BASELINE" # Or verified interview timestamp
  escalate_reason: "Reason text"     # Required if severity is escalate
  answer: "Urdu / Roman Urdu advice spoken in the artisan persona"
```

### Step 2: Vocabulary & Synonym Mapping
When adding support for new colloquial Urdu, Sindhi, or English phrasing:
1. Open [`synonyms.yaml`](synonyms.yaml).
2. Locate the appropriate semantic category or create a new tag.
3. Add regex patterns or word roots with explicit word boundaries (`\b`).
4. Avoid bare substrings that collide with ordinary words (e.g., matching `fire` must not trigger on `fir` or `profile`).

### Step 3: Negation Safety Checks
The engine features a negation analyzer that ignores tags when negated (e.g., *"screen crack nahi hai"* drops `screen_cracked`).
- **Critical Invariant**: Negation must be clause-scoped! Negating a benign symptom (e.g., *"charge nahi ho raha"*) must **never** drop or conceal an active hazard tag (e.g., `battery_swollen`).
- Always run the probe tests in `test_engine.py` when touching tag extraction.

### Step 4: Add Automated Unit Tests
Every new or modified rule requires at least two dedicated test cases in [`test_engine.py`](test_engine.py):
1. English test input.
2. Roman Urdu / Colloquial Urdu test input.
3. If the rule involves a safety stop, verify that `is_safety_stop == True` and `verdict == "ESCALATE"`.

---

## 🎨 Front-End Development Standards

- **Vanilla Stack Only**: [`static/index.html`](static/index.html) must contain all HTML, CSS, and client-side JavaScript in a single, clean file.
- **3D Visual Effects**: Use CSS3 3D transforms (`perspective`, `transform-style: preserve-3d`, `rotateX`, `rotateY`, `translateZ`, `backdrop-filter`).
- **No Heavy Libraries**: Do not import Three.js, Babylon.js, Tailwind, jQuery, Bootstrap, or Axios.
- **Micro-Parallax**: Keep parallax and cursor tracking inside requestAnimationFrame loops with smooth decay interpolation.
- **Accessibility & Contrast**: Ensure text contrast meets WCAG AA standards against dark metallic backgrounds.

---

## 🧪 Testing Guidelines

Before opening a pull request, run the complete verification matrix:

```bash
# 1. Deterministic Rule Engine Test Suite (56+ assertions)
python test_engine.py

# 2. External LLM & Phraser Test Suite
python test_llm.py

# 3. Submission Package Builder (Validates archive integrity)
python package_submission.py
```

---

## 🔄 Pull Request (PR) Checklist

When submitting a Pull Request, ensure the description contains:
1. **Summary of Change**: Concise explanation of what was added or fixed.
2. **Safety Impact**: State clearly whether this affects `ESCALATE` or `safety_stop` paths.
3. **Provenance Statement**: Where did the rule advice come from? (e.g., *"Interview with Ustaad Tariq, Saddar Karachi"* or *"Draft Baseline Rule based on manufacturer datasheets"*).
4. **Test Output**: Paste the terminal output of `python test_engine.py` and `python test_llm.py`.

### Commit Message Conventions
Follow Conventional Commits:
- `feat(engine): add rule for USB-C short circuit detection`
- `fix(synonyms): refine negation regex for battery charging faults`
- `docs(arch): update audio pipeline fallback diagram`
- `style(ui): polish 3d gimbal ring lighting`

---

## 📬 Questions and Contact

For competition queries, technical feedback, or reporting edge-case safety misclassifications:
- Open a GitHub Issue: [github.com/abdulhayykhan/Ustaad-In-A-Box/issues](https://github.com/abdulhayykhan/Ustaad-In-A-Box/issues)
- Developer: **Abdul Hayy Khan** (Dawood University of Engineering & Technology, Karachi)
- Event: **Rocketathon 2026, PK2047, Karachi**
