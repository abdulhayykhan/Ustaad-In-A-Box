# 🎙 Human Capture & Rule Authoring Guide

This guide establishes the standardized procedure for capturing the tacit knowledge of a real repair technician, obtaining valid written consent, and converting recorded interviews into auditable YAML rules for **Ustaad-in-a-Box**.

---

## 1. Ethical Protocol & Technician Consent

Rocketathon Track 1 rules require:
> *"Pick your person first. A stand-in for one real, named person who has agreed to take part... Get their written agreement before you start. The stand-in never claims to be the technician; it identifies itself as his stand-in."*

### Standard Written Consent Form Template
Print or transcribe this agreement on paper or send via WhatsApp/SMS to capture a photographic or digital record before recording:

```text
========================================================================
PARTICIPANT CONSENT AGREEMENT — USTAAD-IN-A-BOX / ROCKETATHON 2026
========================================================================

I, _________________________________________________ [Technician Name],
operating at ______________________________________ [Shop / Market Name],
hereby grant permission to Team DUET to interview me, record my voice,
and extract my diagnostic and safety judgement rules for the project
"Ustaad-in-a-Box" in Track 1 (Stand-In) of Rocketathon 2026.

I understand that:
1. The machine will explicitly represent itself as my STAND-IN, not as me.
2. It will only deliver diagnostic safety advice that I have reviewed.
3. Any question outside my captured rules will be directed back to me.
4. My recordings will be used solely for rule verification and academic/
   hackathon demonstration purposes.
5. No financial claims or liabilities are created by this participation.

Technician Signature / Confirmation: __________________________________
Date & Time: ___________________________________________________________
Phone Number: __________________________________________________________
Witness / Team Lead: ___________________________________________________
========================================================================
```

---

## 2. The 3-Hour Semi-Structured Interview Script

Conduct the interview at their workshop bench where they have physical tools and customer devices in hand. Record the audio with an explicit counter timer running.

### Module 1: Hard Safety Stops & Emergency Boundaries (45 mins)
- *"What is the single most dangerous thing a customer does when their phone gets hot?"*
- *"When a battery starts swelling (phoolna), what happens if they keep charging it?"*
- *"What should a customer NEVER do if liquid spills on their device?"*
- *"Have you ever had a power bank or battery catch fire or smoke in your shop? What triggered it?"*
- *"What equipment do you refuse to open yourself without industrial safety gear?"*

### Module 2: The Grey Zone — Caution vs Immediate Replacement (60 mins)
- *"When is a cracked screen just cosmetic, and when is it dangerous or about to kill the display?"*
- *"How can a customer tell the difference between a broken charging port and a bad cable at home?"*
- *"If a phone battery drops from 50% to 10% in ten minutes, is it the battery cell or the motherboard power IC?"*
- *"What are the common causes of laptop thermal throttling in Karachi summers?"*
- *"What is your personal formula for 'Repair vs Replace' when a customer brings an old phone?"*

### Module 3: Edge Cases, Clarifying Questions & Limits (45 mins)
- *"If a customer asks you to unlock or bypass a pattern lock, what do you tell them?"*
- *"What do you say when someone asks for medical advice about radiation or 5G?"*
- *"When do you tell a customer: 'I cannot fix this, take it to the authorized distributor'?"*

### Module 4: Speech Mannerisms, Greetings & Closings (30 mins)
- Note their natural openings: *"Bhai jaan..."*, *"Yaar dekho..."*, *"Seedhi baat yeh hai..."*
- Note how they explain technical components in Roman Urdu (*"IC garam ho rahi hai"*, *"Patta kat gaya"*).

---

## 3. Authoring `rules.yaml`

Every confirmed rule must follow this schema:

```yaml
- id: BAT-003                       # Unique Category-Number code
  label: "Swollen battery"          # Human readable descriptor
  when: [battery_swollen]           # Array of symptom tags (AND logic)
  severity: safety_stop             # safety_stop | caution | normal
  verdict: ESCALATE                 # SAFE | CAUTION | ESCALATE
  say: >                            # The technician's authentic spoken wording
    Yaar, swollen battery serious cheez hai. Abhi charging band karo aur
    phone use karna bhi chhoro. Isko mat dabao, mat kholne ki koshish karo.
    Mujhse milne aao — swollen battery leak ya catch fire kar sakti hai.
  escalate: true                    # Boolean flag for escalation
  reason: "Swollen battery can leak, catch fire, or explode. Stop use immediately."
  source: "Interview 1, 00:14:22"   # Mandatory timestamp in interview audio
```

### Rule Authoring Rules
1. **Source Timestamp is Mandatory:** Never create a rule without an exact timestamp (`Interview X, HH:MM:SS`). If a rule cannot be traced to the recording, it cannot be added.
2. **`safety_stop` Forces Escalation:** Any rule marked `severity: safety_stop` must have `verdict: ESCALATE` and `escalate: true`.
3. **Compound Conditions:** If a rule depends on two symptoms (e.g. wet AND still turned on), declare both in `when`:
   ```yaml
   when: [water_damage, device_on]
   ```

---

## 4. Expanding `synonyms.yaml`

When adding vernacular phrases, follow these rules:
1. **Lowercase Only:** Regex matching applies `re.IGNORECASE`, so write all entries in lowercase.
2. **Include Common Transliterations:**
   - Urdu speakers transcribe phonetic sounds differently in Roman Urdu:
     - *"phoolna"*, *"phula"*, *"foola"*, *"pholi"*
     - *"paani"*, *"pani"*
     - *"dhuan"*, *"dhuwan"*, *"smoke"*
3. **Avoid Overly Broad Single Words:** Do not use solitary generic words like `"on"`, `"and"`, or `"water"` as synonyms, because they cause false triggers in innocent phrases (e.g. `"water"` triggers on `"battery drains like water"`). Use phrases like `"pani gira"` or `"got wet"`.

---

## 5. Adding & Running Automated Regression Tests

Before any new rule is committed, add test cases to `test_engine.py`:

```python
TESTS = [
    # Format: (Description, Input Text, Expected Verdict, Expected Rule ID)
    ("BAT-005 en: battery punctured", "my battery got punctured", "ESCALATE", "BAT-005"),
    ("BAT-005 ro: battery soorakh",   "battery me soorakh ho gaya", "ESCALATE", "BAT-005"),
]
```

Run the suite in your terminal:
```bash
python -X utf8 test_engine.py
```
**All tests must pass (`0 failed`) before taking the system to the judging table.**
