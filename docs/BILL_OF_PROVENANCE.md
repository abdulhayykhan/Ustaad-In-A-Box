# 📋 Rocketathon 2026 · Deliverable 02: Bill of Provenance

**Project:** Ustaad-in-a-Box  
**Track:** Track 1: Stand-In  
**Team:** Dawood University of Engineering & Technology (DUET)  
**Date:** 29 September 2026  
**Venue:** Expo Centre Karachi  

---

## 1. Declarative Statement on the Scrap Rule

> **"Everything you build must come from scrap, e-waste, donated or recycled parts. You may not buy parts or pay for services."**

We hereby certify that **PKR 0.00** was spent on hardware components, commercial software licenses, cloud compute, or paid API subscriptions for the creation and operation of **Ustaad-in-a-Box**. Every physical item was salvaged from home surplus, family e-waste drawers, or local mobile repair workshops. Every software dependency is licensed under permissive, royalty-free Open Source licenses.

---

## 2. Hardware Bill of Provenance

| Component & Role | Previous Life / What It Was | Origin / Where It Came From | Next Life / Where It Goes After | Inspection & Safety Status |
|---|---|---|---|---|
| **Host Compute & Engine** (Laptop Brain) | 2017 Lenovo IdeaPad 320 with cracked chassis and dead internal battery (operates solely on AC brick). | Team member's family surplus (discarded after hinge damage). | Retained by team for educational robotics and open-source lab projects. | Internal battery safely disconnected. Powered via original inspected DC adapter. No swollen cells. |
| **User Interface & Face Display** (Old Android Phone) | 2018 Samsung Galaxy J6 with spiderweb cracked outer glass, functional AMOLED display and capacitive touch. | Donated by neighborhood repair shop (Saddar mobile market scrap bin). | Returned to repair shop scrap bin or recycled via Alkhidmat e-waste drive. | Battery physically inspected by mentor: 0% swelling, 0% denting, voltage nominal (3.8V). |
| **Voice Output / Speaker** (Acoustic presence) | 3W audio transducer removed from a broken Bluetooth portable speaker with a dead micro-USB port. | Common Scrapyard / Team electronic scrap box. | Returned to common scrapyard for future hackathons. | Stripped of faulty battery; powered directly from salvaged laptop USB 5V rail. |
| **Microphone / Acoustic Input** | Integrated stereo microphone array inside Lenovo laptop lid. | Native to salvaged laptop. | Stays with laptop chassis. | Passed bench audio test. No hazardous voltages. |
| **Chassis Stand / Mounting** | Discarded cardboard packing crate, scrap wooden strip, and rubber bands. | DUET workshop recycling bin. | Recycled in paper waste stream. | Non-conductive, clean, no sharp metal edges. |
| **Cabling & Power Delivery** | Used USB-A to Micro-USB cables and laptop DC barrel adapter. | Personal tool kit (pre-owned). | Returned to team personal tools. | Insulation inspected with multimeter; zero frayed wiring or exposed conductors. |

---

## 3. Software Bill of Provenance & Licenses

All software used in this project is 100% free, local, open-source, and does not require active cloud connections or commercial API keys.

| Software / Package | Version | Purpose in System | License | Upstream Origin |
|---|---|---|---|---|
| **Python** | `3.14.3` | Core application runtime & rule engine execution | PSF License | [python.org](https://www.python.org/) |
| **FastAPI** | `0.135.1` | Asynchronous local REST API and HTTP server | MIT License | [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) |
| **Uvicorn** | `0.41.0` | High-performance ASGI web server | BSD 3-Clause | [uvicorn.org](https://www.uvicorn.org/) |
| **PyYAML** | `6.0.3` | Parsing human-readable rule and synonym definitions | MIT License | [pyyaml.org](https://pyyaml.org/) |
| **Pydantic** | `2.12.5` | Data validation, type safety, and schema models | MIT License | [pydantic.dev](https://docs.pydantic.dev/) |
| **faster-whisper** (optional local STT) | `latest` | CPU-quantized int8 multilingual speech-to-text | MIT License / Apache 2.0 | Systran / OpenAI Whisper weights |
| **Web Speech API** | Native Browser | Zero-latency Urdu/Hindi/English local voice synthesis | W3C Standard | Embedded in Chromium / WebKit engine |
| **Vanilla HTML5 / CSS3 / ES6** | Handcrafted | Push-to-talk interface, waveform canvas, why-panel | MIT (Custom) | Authored locally by team |

---

## 4. Disassembly and Circular Lifecycle Plan

In accordance with Rocketathon rules on circularity:
1. **Zero-Adhesive Construction:** All components are affixed using non-destructive mechanical friction, rubber bands, or reusable cable ties. No hot glue or epoxies were applied to electronic boards.
2. **Immediate Post-Event Reclamation:**
   - The salvaged Samsung smartphone will be factory wiped, dismounted, and handed back to the donating repair workshop for component harvesting (PMIC, camera modules).
   - Cardboard mounting brackets will be sorted into DUET paper recycling bins.
   - The host laptop will return to serving student terminal sessions in the university hardware lab.
