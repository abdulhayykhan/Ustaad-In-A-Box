# 🎙 Human Knowledge Capture & Rule Authoring Guide

This guide establishes the rigorous, standardized methodology for capturing the tacit diagnostic instincts of a veteran repair technician, obtaining ethical informed consent, formalizing vernacular Roman Urdu into YAML rule specifications, and verifying decisions against real-world hardware failure modes for **Ustaad-in-a-Box**.

---

## 1. Ethical Protocol & Technician Consent

Rocketathon 2026 Track 1 (Stand-In) explicitly mandates:
> *"Pick your person first. A stand-in for one real, named person who has agreed to take part... Get their written agreement before you start. The stand-in never claims to be the technician; it identifies itself as his stand-in."*

### Standard Written Consent Form Template
Print or transcribe this agreement on paper or send via WhatsApp/SMS to capture an immutable photographic or digital record before recording:

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

## 2. Standard Rule ID Taxonomy

All diagnostic rules must adhere to the standardized prefix schema:

| Prefix | Domain | Severity Standard | Examples |
|---|---|---|---|
| `BAT-` | Battery Health & Chemical Hazards | `safety_stop` / `caution` | Swollen cells, punctures, rapid drain, thermal swelling |
| `WAT-` | Liquid Immersion & Moisture | `safety_stop` / `caution` | Submerged while powered on, hair-dryer usage, corrosion |
| `CHG-` | Charging Ports, Cables & Adapters | `safety_stop` / `caution` | Burning smell in port, overheating charger, loose pin |
| `SCR-` | Display, Digitizer & Glass | `caution` / `normal` | Spiderweb hairline crack, touch unresponsive, purple ink bleed |
| `DEV-` | Motherboard, Power IC & SoC | `safety_stop` / `caution` | Standby overheating, boot loops, sudden shutdown |
| `LAP-` | Laptop Thermal & Fan Systems | `caution` / `normal` | Thermal throttling, blocked vents, dry thermal paste |
| `PWR-` | Power Banks & External Batteries | `safety_stop` | Bulging casing, DIY tampering, extreme heat during charging |
| `SMK-` | Combustion, Fumes & Arcing | `safety_stop` (Always ESCALATE) | Visible smoke, toxic acrid odor, popping electrical sparks |
| `REP-` | Economic Repair vs. Replace | `normal` (SAFE / Advice) | Cost exceeds 50% device value, obsolete architecture |
| `OOS-` | Out of Scope Inquiries | `ESCALATE` (Out-of-Scope) | Pricing negotiation, iCloud/IMEI bypass, medical advice |

---

## 3. The 3-Hour Semi-Structured Interview Script

Conduct the interview at the technician's actual repair workbench. Keep physical tools, broken motherboards, and swollen battery packs on hand as tactile prompts.

### Module 1: Hard Safety Stops & Fire Hazards (45 mins)
- *"Jab battery phoolna shuru hoti hai, log aksar sochte hain back cover band ho jaye toh theek hai. Aap unhein kya samjhayenge?"*
- *"Agar koi mobile paani mein gir jaye aur customer usko hairdryer se sukhaye ya charger laga de, toh motherboard pe kya hota hai?"*
- *"Aap ne kabhi power bank ya phone phat te dekha hai shop pe? Aag lagne se pehle pehla sign kya hota hai?"*
- *"Kaunse aese masle hain jinpe aap customer ko kehte hain ke phone ko haath bhi mat lagao aur foran shop le aao?"*

### Module 2: The Grey Zone — Caution vs. Cosmetic (60 mins)
- *"Agar screen pe sirf baal barabar crack ho lekin touch theek chal raha ho, toh kya customer usko chala sakta hai?"*
- *"OLED screen pe purple ya black ink ka daagh fail raha ho, toh kya woh theek ho sakta hai ya poora panel badalna padega?"*
- *"Agar phone charging pe lagaye baghair bhi standby pe garam ho raha ho, toh yeh battery ka masla hai ya charging IC short hai?"*
- *"Karachi ki garmi mein laptops aksar band ho jaate hain. Fan saaf karne se kaam ban jata hai ya heat sink dry ho jata hai?"*

### Module 3: Boundaries & Scope Enforcement (45 mins)
- *"Agar koi aapse pattern lock ya iCloud bypass karwane aaye, aap unko kya jawab dete hain?"*
- *"Phone repair ka estimate phone pe kyun nahi dena chahiye jab tak board physical inspect na ho?"*

### Module 4: Dialect & Persona Nuances (30 mins)
- Note natural conversational colloquialisms:
  - *"Bhai jaan, seedhi baat yeh hai..."*
  - *"IC garam ho rahi hai..."*
  - *"Patta kat gaya hai display ka..."*
  - *"Isko dabana mat, warna cell puncture ho jayega..."*

---

## 4. Authoring YAML Rules (`rules.yaml`)

Every rule must conform to this schema in [`rules.yaml`](rules.yaml):

```yaml
- id: BAT-003
  label: "Swollen battery"
  when: [battery_swollen]
  severity: safety_stop
  verdict: ESCALATE
  safety_stop: true
  say: >
    Yaar, swollen battery serious cheez hai. Abhi charging band karo aur
    phone use karna bhi chhoro. Isko mat dabao, mat kholne ki koshish karo.
    Mujhse milne aao — swollen battery leak ya catch fire kar sakti hai.
  escalate: true
  reason: "Swollen battery can leak, catch fire, or explode. Stop use immediately."
  source: "DRAFT RULE — UNVERIFIED BASELINE (Pending Technician Interview)"
```

### The 4 Non-Negotiable Authoring Laws:
1. **The Provenance Mandate**: Never fabricate an interview timestamp! If the rule is a heuristic baseline waiting for the live interview recording, write:  
   `source: "DRAFT RULE — UNVERIFIED BASELINE (Pending Technician Interview)"`.  
   Once recorded, update to the exact tape counter: `Interview Tariq 2026-09-30, 00:14:22`.
2. **`safety_stop` Forces Escalation**: Any rule where `safety_stop: true` MUST declare `severity: safety_stop`, `verdict: ESCALATE`, and `escalate: true`.
3. **Compound Preconditions**: If a rule triggers only when two concurrent events occur (e.g. wet AND on), declare both in `when`:
   ```yaml
   when: [water_damage, device_on]
   ```
4. **No Hallucinated DIY Advice**: Under no circumstance should a rule instruct an untrained customer to prick, compress, or submerge a damaged battery in rice.

---

## 5. Expanding Synonyms & Dialect Mapping (`synonyms.yaml`)

When adding colloquial terms:
1. **Lowercase Everywhere**: Tag matching is case-insensitive.
2. **Enforce Word Boundaries (`\b`)**: Never enter bare substrings that could collide with harmless words:
   - ❌ Bad: `"fire"` (Matches `"firefox"`, `"bonfire"`, `"profile"`)
   - ✅ Good: `"\bfire\b"`, `"\baag lag\b"`, `"\bjalne\b"`
3. **Cover Transliteration Variants**:
   - `phooli`, `pholi`, `phool gaya`, `bulging`, `swollen`, `sujan`
   - `dhuwan`, `dhuan`, `smoke`, `smell`, `boo aa rahi`
   - `screen toot`, `screen break`, `toota hua glass`

---

## 6. Verification & Automated Unit Testing

Whenever a rule or synonym is touched, write at least two new unit tests in [`test_engine.py`](test_engine.py):

```python
# In test_engine.py:
TESTS.extend([
    ("BAT-005 en: battery punctured", "my phone battery was punctured by a nail", "ESCALATE", "BAT-005"),
    ("BAT-005 ro: battery me soorakh", "battery me soorakh ho gaya hai smell aa rahi", "ESCALATE", "BAT-005"),
])
```

Execute the full test harness:
```bash
python test_engine.py
python test_llm.py
```
**Zero test failures are permitted before deployment.**
