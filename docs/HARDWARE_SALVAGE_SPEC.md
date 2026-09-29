# Ustaad-in-a-Box · Hardware Salvage & E-Waste Build Specification

**Event:** Rocketathon 2026, PK2047, Karachi  
**Track:** 1, Stand-In  
**Theme:** Scrap Hardware, E-Waste Reduction & Safe Electronics Triage  

---

## 🔩 1. Physical Salvage Philosophy

In Pakistan's informal electronics hubs (such as Karachi's Regal Chowk, Saddar, and Shershah Scrap Market), thousands of discarded laptops, fractured phone chassis, and damaged lithium battery packs are stripped down for raw materials every day. 

**Ustaad-in-a-Box** proves that functional, life-saving diagnostic intelligence does not require multi-thousand-dollar cloud servers. It breathes a second life into salvaged e-waste components by running a lightweight deterministic safety engine on discarded hardware.

---

## 🛠️ 2. Bill of Salvaged Materials (BoM)

The exhibition physical stand is constructed entirely from reclaimed scrap:

| Item | Original Source | Scrap Cost (PKR) | Purpose in Stand |
|---|---|---|---|
| **Host Motherboard & CPU** | Discarded Dell Inspiron 1545 (broken hinges, dead screen) | Free (Salvaged from e-waste bin) | Executes FastAPI server, deterministic rule engine, and audio pipeline |
| **Cooling Fan** | 5V DC blower fan extracted from discarded DVD player | 100 PKR | Auxiliary cooling over CPU heatsink |
| **Secondary Display** | 10.1" salvage LCD panel from broken netbook via LVDS driver board | 800 PKR | Public diagnostic readouts and 3D UI kiosk |
| **Microphone Capsule** | Electret condenser microphone harvested from broken smartphone hands-free headset | 50 PKR | Push-to-talk speech input with salvage foam pop filter |
| **Speaker Unit** | 3W 4Ω magnetic transducer from a broken CRT television | 150 PKR | Text-to-speech Urdu audio announcements |
| **Stand Enclosure** | Reclaimed clear acrylic offcuts and recycled aluminum heatsink fins | Free (Workshop scrap) | Transparent protective chassis revealing salvaged circuit boards |
| **Battery Quarantine Chamber** | Repurposed steel military ammunition canister with fireproof ceramic wool lining | 500 PKR | Live demonstration of physical containment for swollen lithium batteries |

**Total Salvage Hardware Cost:** **1,600 PKR (~$5.75 USD)**

---

## ⚡ 3. Battery Safety Quarantine & Thermal Management

Because Track 1 specifically addresses battery degradation, swelling, and fire prevention, the physical stand incorporates an active physical safety enclosure:

```
+-------------------------------------------------------------+
|               USTAAD-IN-A-BOX SALVAGE STAND                 |
|                                                             |
|   +-----------------------+     +-----------------------+   |
|   |   Holographic 3D UI   |     | Push-to-Talk 3D Disc  |   |
|   |    (Netbook Screen)   |     |    (Reclaimed Mic)    |   |
|   +-----------------------+     +-----------------------+   |
|                                                             |
|   +-----------------------------------------------------+   |
|   |   STEEL QUARANTINE CHAMBER (Swollen Battery Safe)    |   |
|   |   - Sand / Vermiculite fire suppressant layer       |   |
|   |   - Overpressure relief valve                       |   |
|   |   - High-temperature ceramic thermal insulation     |   |
|   +-----------------------------------------------------+   |
|                                                             |
|   +-----------------------------------------------------+   |
|   |   Salvaged Dell Inspiron Motherboard (Core 2 Duo)    |   |
|   +-----------------------------------------------------+   |
+-------------------------------------------------------------+
```

### Safety Quarantine Rules:
1. **No Live Charging of Suspect Packs**: Any device or battery presenting symptoms of physical swelling (gas pouch expansion) is strictly forbidden from connecting to electrical charging circuits inside the booth.
2. **Immediate Steel Isolation**: In live booth triage, if a participant presents a bulging phone, it is transferred immediately into the sand-lined steel canister.
3. **Overpressure Venting**: The quarantine box features directional top exhaust vents lined with non-combustible ceramic wool to prevent shrapnel propagation in the event of cell rupture.

---

## 🔌 4. Electrical Power Architecture

The entire salvage stand is powered via a single 12V 5A DC switching power supply extracted from a discarded desktop monitor:
- **12V Bus**: Powers the netbook LVDS display controller and audio power amplifier.
- **Buck Converter Step-Down (5V / 3A)**: Powers the auxiliary cooling fans and USB microphone preamplifier.
- **Power Consumption**: Under full load (CPU processing STT + screen running 3D canvas), the total system draws **less than 28 Watts**.
