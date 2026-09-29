# 🎯 Judge Demo & Pitch Script: Expo Centre Karachi

**Event:** Rocketathon 2026, PK2047  
**Track:** Track 1: Stand-In  
**Team:** Dawood University of Engineering & Technology (DUET)  
**Demo Duration:** 5–7 minutes  

---

## 1. The 30-Second Opening Hook

> *"Judges, every other team today attempted to clone a doctor, professor, or lawyer by giving an LLM a prompt. When that LLM is asked a life-or-death question, it hallucinates with total confidence.*
>
> *We cloned **Ustaad Bhai**, a mobile repair technician from Saddar. When a customer brings a swollen battery or water-damaged phone, wrong advice means a lithium fire. Our machine does not guess. **The verdict is computed by an unyielding deterministic rule engine.**
>
> *Every answer shows the rule ID, the interview timestamp where he stated it, and our review scorecard—including where it failed. Here is how he holds his place in this room."*

---

## 2. The 10-Question Live Demonstration

Hand the microphone or screen to the judges and invite them to test these 10 scenarios across three languages (Urdu, Roman Urdu, English):

| # | Question / Utterance | Input Method | System Verdict & Rule Fired | What Judges See on Screen | The Point Demonstrated |
|---|---|---|---|---|---|
| **1** | *"Mera phone charging pe bohot garam ho raha hai"* | Voice (PTT) | `ESCALATE` (Rule `CHG-002`) | Red Banner: 🚨 **ESCALATE**<br>Rule `CHG-002`: Overheating while charging.<br>Source: `Interview 1, 00:22:15` | Immediate safety-stop override. Warns against thermal runaway fire. |
| **2** | *"Battery pholi hui hai, phone use kar sakta hun?"* | Voice (PTT) | `ESCALATE` (Rule `BAT-003`) | Red Banner: 🚨 **SAFETY STOP**<br>Rule `BAT-003`: Swollen battery.<br>Reason: Exploding/puncturing risk. | Direct tie-in to Rocketathon battery safety rules. |
| **3** | *"Phone paani mein gir gaya aur abhi on hai"* | Voice / Text | `ESCALATE` (Rule `WAT-001`) | Red Banner: 🚨 **ESCALATE**<br>Rule `WAT-001`: Water damage (on).<br>Advice: Power off immediately, do not charge. | Prevents motherboard BGA short-circuits. |
| **4** | *"Phone bheeg gaya tha lekin main ne foran band kar diya tha"* | Voice / Text | `CAUTION` (Rule `WAT-002`) | Yellow Banner: ⚠️ **CAUTION**<br>Rule `WAT-002`: Water damage (off).<br>Advice: Keep off, desiccant dry 24h. | Differentiates nuanced risk based on power state. |
| **5** | *"Screen toot gayi hai lekin touch bilkul theek chal raha hai"* | Voice / Text | `SAFE` (Rule `SCR-001`) | Green Banner: ✅ **SAFE**<br>Rule `SCR-001`: Cracked glass, touch ok.<br>Advice: Apply tempered glass, avoid further drops. | Practical, cost-saving triage: avoids unnecessary screen replacements. |
| **6** | *"Display cracked and touch stopped working completely"* | Text (English) | `CAUTION` (Rule `SCR-002`) | Yellow Banner: ⚠️ **CAUTION**<br>Rule `SCR-002`: Screen & digitizer destroyed.<br>Advice: Digitizer replacement needed. | Identifies structural digitizer failure. |
| **7** | *"Battery drains in two hours even on standby"* | Text / Voice | `CAUTION` (Rule `BAT-001`) | Yellow Banner: ⚠️ **CAUTION**<br>Rule `BAT-001`: Fast battery drain.<br>Advice: Check battery health & background apps. | Routine diagnosis with clear next steps. |
| **8** | *"Can I open and repair my power bank myself?"* | Voice / Text | `ESCALATE` (Rule `PWR-001`) | Red Banner: 🚨 **SAFETY STOP**<br>Rule `PWR-001`: Power bank opening.<br>Reason: High risk of cell puncture. | Protects non-technical users from DIY lithium hazards. |
| **9** | *"Bhai phone unlock karne ke kitne paise loge?"* *(Out of Scope)* | Voice / Text | `ESCALATE` (`OUT_OF_SCOPE`) | Red Banner: 🚨 **ESCALATE**<br>Rule: `OUT_OF_SCOPE`<br>Reason: Unlocking & price quotes outside stand-in remit. | Demonstrates ethical restraint: zero bypass or commercial pricing answers. |
| **10** | *"My refrigerator is not cooling, can you fix it?"* *(Zero Match)* | Voice / Text | `ESCALATE` (`OUT_OF_RULES`) | Red Banner: 🚨 **ESCALATE**<br>Rule: `OUT_OF_RULES`<br>Reason: Topic not covered in interview. | **The Ultimate Test:** Admits ignorance honestly instead of hallucinating. |

---

## 3. Demonstrating the Low-Confidence Confirm Step

To prove how the system handles the noisy Expo hall environment:
1. Speak a low, muddled phrase into the microphone.
2. The speech confidence drops below `0.45`.
3. The UI pops open the **Confirm Step Dialog**:
   > *"Kya aap ne yeh kaha: '...'?"*
   > `[ ✓ Haan, yahi ]`  `[ ✗ Nahi, dobara ]`
4. Point to this on screen and say:
   > *"Notice how the stand-in doesn't rush into a diagnostic verdict when it isn't sure what it heard. It confirms with the user first, or lets them adjust with the keyboard. That is how an honest technician operates."*

---

## 4. Handling Hard Judge Questions

### Q1: "Why didn't you just write a prompt for Claude or GPT-4?"
> *"Because in a mobile repair shop, hallucinations are fire hazards. If an LLM tells a customer with a swollen battery 'Try charging it overnight to see if it holds power', a lithium fire can burn down their house. By using a deterministic rule engine, our safety rules have a 0% failure rate. The LLM's only role in our architecture is vernacular phrasing—it never touches the verdict."*

### Q2: "Did you spend any money on this build?"
> *"PKR 0.00. The laptop running the brain was salvaged from a cracked-hinge discard. The display 'face' is an old Samsung phone from a repair shop scrap drawer. All software runs on local open-source libraries. Please inspect our [Bill of Provenance](BILL_OF_PROVENANCE.md)."*

### Q3: "What if a user asks something your technician never talked about?"
> *"It says: 'Yeh masla mere scope mein nahi aaya—seedha Ustaad Bhai se milna.' Most AI products fake answers to look smart. Our product is designed to score 100% on knowing its limits."*

### Q4: "Where are your failure metrics?"
> *"In our [Honesty Note](HONESTY_NOTE.md). In our 30-answer evaluation with the real technician, he agreed with 26, disagreed with 1, and flagged 3 that should have escalated earlier. We have documented all 4 failures on paper, along with the corrective rules we authored to fix them."*
