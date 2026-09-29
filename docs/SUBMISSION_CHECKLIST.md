# 🏁 Final Submission Checklist & Event Day Playbook

**Event:** Rocketathon 2026, PK2047  
**Venue:** Expo Centre Karachi  
**Track:** Track 1: Stand-In  
**Team:** Dawood University of Engineering & Technology (DUET)  

---

## 📌 Deliverables Summary & Exact File Locations

| # | Deliverable | Status | File Location | Key Content to Highlight to Judges |
|---|---|---|---|---|
| **01** | **Live Working Demo** | Ready & Running | Web UI: `http://localhost:8000` | 100% offline, Push-to-Talk, live transcription, deterministic rule resolution, Why-panel showing Rule ID and interview source timestamp. |
| **02** | **Bill of Provenance** | Completed | [`docs/BILL_OF_PROVENANCE.md`](BILL_OF_PROVENANCE.md) | PKR 0.00 spent. Complete audit of salvaged 2017 Lenovo laptop, cracked Samsung phone, recycled transducer speaker, and open-source licenses. |
| **03** | **One-Page Honesty Note** | Completed | [`docs/HONESTY_NOTE.md`](HONESTY_NOTE.md) | 30-answer technician review scorecard ($86.7\%$ agree), documented 4 edge cases with remediations, and Section 4.2 live bench test analysis. |

---

## 🧰 Physical Table Setup at Expo Centre Karachi

Follow this setup order before the judges arrive at your booth:

1. **Hardware Placement:**
   - **Brain:** Place the salvaged laptop open or flat behind your display area, plugged into AC power (do not rely on failing internal batteries).
   - **Face (Stand-In Display):** Prop the salvaged Samsung smartphone against the cardboard mount facing the audience. 
   - **Network Setup:** If connecting the phone wirelessly, enable the laptop's mobile hotspot (no internet required). On the phone's browser, open `http://<LAPTOP_LOCAL_IP>:8000`.
   - **Audio:** Plug in the salvaged speaker and test audio levels. Set volume to ~80% so speech is audible over hall noise without clipping.

2. **Bench Sanity Test (Run 60 seconds before judging):**
   - Click the Push-to-Talk mic or type:
     > *"battery pholi hui hai"*
   - Verify the screen immediately displays:
     - 🚨 **ESCALATE / SAFETY STOP**
     - Rule **`BAT-003`**
     - Interview Source: `Interview 1, 00:14:22`
   - Click the "Why?" tab in the sidebar and ensure tags and reason populate cleanly.

3. **Printed / Tablet Materials on Table:**
   - Keep a printout or tablet copy of [`BILL_OF_PROVENANCE.md`](BILL_OF_PROVENANCE.md).
   - Keep a printout or tablet copy of [`HONESTY_NOTE.md`](HONESTY_NOTE.md).
   - Have the technician's signed consent form (or WhatsApp screenshot on phone) ready for inspection.

---

## 🎙️ 2-Minute Elevator Pitch (When Judges First Walk Up)

> *"Assalam-o-Alaikum judges! We are Team DUET for Track 1: Stand-In.
>
> Every other team here built a chatbot that claims to be a teacher or doctor. But in high-risk triage, a generative LLM that hallucinates is dangerous.
>
> We cloned **Ustaad Bhai**, a mobile repair technician from Saddar. When a customer has a swollen lithium battery, water damage, or thermal runaway, wrong advice causes a house fire.
>
> Our system is built **100% from scrap hardware for PKR 0.00**. Its verdicts are computed by an **unyielding deterministic rule engine**—never an AI model's guess. Every answer displays the exact rule ID, the interview timestamp where he stated it, and our transparent honesty scorecard.
>
> Here, please ask it any question about a damaged phone in Urdu, Roman Urdu, or English."*

---

## ⚡ The 5 Core Judge Scenarios to Run Live

Run these sequentially from [`docs/DEMO_SCRIPT.md`](DEMO_SCRIPT.md):

1. **Catastrophic Battery Safety Stop:**
   - Input: *"battery pholi hui hai phone use karun?"*
   - Shows: `BAT-003` (`ESCALATE`), Red Banner, Explains fire risk.
2. **Thermal Runaway on Charger:**
   - Input: *"phone charging pe buht zaada garam hora hai"*
   - Shows: `CHG-002` (`ESCALATE`), Instructs immediate unplugging.
3. **Nuanced Water Damage Triage:**
   - Input: *"mobile paani mai gir gya haii"*
   - Shows: `WAT-002` (`CAUTION`), Instructs keeping power off and desiccant drying.
4. **General Screen Triage:**
   - Input: *"screen toot gyi hai mobile ki"*
   - Shows: `SCR-000` (`CAUTION`), Checks touch state before recommending replacement.
5. **Knowing Its Limits (Out of Scope / Zero Match):**
   - Input: *"can you unlock pattern lock"* or *"fridge repair kardo"*
   - Shows: `OUT_OF_SCOPE` or `OUT_OF_RULES` (`ESCALATE`), Transparently admits limits.

---

## 🛡️ Emergency Contingency Checklist

| Failure Mode | Immediate Emergency Fix |
|---|---|
| **Expo hall Wi-Fi blocks connections** | The app is 100% offline. Use the laptop screen directly at `http://localhost:8000`, or create an offline local hotspot from the laptop with no internet. |
| **Microphone picks up loud hall announcements** | Switch seamlessly to typed input in the text box below the mic. The rule engine, "Why" panel, and verdict cards remain identical. |
| **Accidental browser tab close** | Re-open browser and go to `http://localhost:8000`. The server is running as a daemon service in the background and preserves history. |
| **Server process terminated** | Double click `run.bat` on the Desktop. It runs all 39 tests in 2 seconds and re-launches the server immediately. |
