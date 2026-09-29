# Ustaad-in-a-Box · Deployment & Operations Guide

This guide provides exhaustive, battle-tested deployment instructions for running **Ustaad-in-a-Box** in production, exhibition booths, or repair shop counters.

The system is designed to run reliably on two fundamentally different hardware tiers:
1. **Tier 1: Salvaged Scrap Hardware (Air-Gapped / Offline)**: A discarded 2011–2014 laptop (Intel Core 2 Duo or 2nd-gen Core i3, 4GB RAM, no GPU, no internet connection).
2. **Tier 2: Cloud Hybrid Station**: A modern workstation, Raspberry Pi 5, or laptop connected to the Groq Cloud API for conversational LLM phrasing and cloud Whisper STT.

---

## 🏗️ Hardware Architecture & Minimum Specifications

| Component | Minimum Salvage Spec (Offline Mode) | Recommended Booth Spec (Hybrid Mode) |
|---|---|---|
| **CPU** | Dual-Core x86_64 (e.g. Intel Core 2 Duo T6600 @ 2.2GHz) | Quad-Core ARM64 or x86_64 (e.g. Raspberry Pi 4/5 or Intel i5) |
| **RAM** | 4 GB DDR2/DDR3 | 8 GB DDR4 |
| **Storage** | 20 GB HDD (Mechanical 5400 RPM supported) | 16 GB SSD / High-Speed microSD |
| **Microphone** | Salvaged 3.5mm TRRS condenser mic or USB webcam mic | Directional USB boundary microphone |
| **Audio Output** | Internal scrap laptop speaker or 3.5mm passive speaker | External amplified desk speaker |
| **Display** | 1024×768 LCD panel (built-in or salvaged external monitor) | 1080p touch monitor or tablet browser |
| **Network** | **Zero / Completely Air-Gapped** | 2 Mbps Wi-Fi or Ethernet |

---

## ⚡ Deployment Modes

### Mode A: 100% Offline Air-Gapped Setup
Ideal for remote disaster recovery camps, e-waste salvage yards, or competition tracks requiring zero external API dependencies.

1. **Rule Engine**: Runs deterministic Python code directly in-memory (< 40 MB RAM footprint).
2. **Speech-to-Text**: Local `faster-whisper` using CPU INT8 quantization (`tiny` or `base` model).
3. **Text-to-Speech**: Browser-native Web Speech API (`window.speechSynthesis`) using installed OS regional voices (Urdu/Hindi/English).
4. **Latency**:
   - Rule Decision: **< 1.5 milliseconds**.
   - Local STT (Audio query): ~1.2 to 2.5 seconds on dual-core CPU.
   - Total roundtrip: **< 2.6 seconds**.

### Mode B: Groq Cloud Hybrid Setup
Ideal for live public interactive demos where maximum conversational charm, authentic Karachi vernacular phrasing, and instantaneous voice transcription are desired.

1. **Rule Engine**: Runs locally on device with absolute decision authority.
2. **LLM Phraser**: Cloud Groq API (`qwen/qwen3.8-27b`) rephrases the verdict in artisan Roman Urdu / English (< 350 ms).
3. **Cloud Whisper**: Cloud Groq Whisper (`whisper-large-v3-turbo`) transcribes speech in < 450 ms.
4. **Resilience**: If the internet cable is unplugged mid-demo, the server automatically drops back to the local deterministic rule engine in 0 ms.

---

## 📥 Step-by-Step Installation

### 1. Operating System Preparation

#### Debian / Ubuntu / Linux Mint:
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv ffmpeg git curl
```

#### Windows 10 / 11:
1. Install Python 3.10+ from [python.org](https://www.python.org/downloads/) (Ensure *"Add python.exe to PATH"* is checked).
2. Install `ffmpeg` (recommended for local audio decoding) or use Windows Media codecs.

---

### 2. Repository Setup

```bash
git clone https://github.com/abdulhayykhan/Ustaad-In-A-Box.git
cd Ustaad-In-A-Box
```

### 3. Virtual Environment Setup

```bash
python3 -m venv venv

# Linux / macOS:
source venv/bin/activate

# Windows PowerShell:
.\venv\Scripts\Activate.ps1
```

### 4. Dependency Installation

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

*Note for Offline Deployment*: If installing on an air-gapped laptop, build a wheel cache beforehand:
```bash
# On an internet-connected machine:
pip download -r requirements.txt -d ./wheels
# On the target air-gapped machine:
pip install --no-index --find-links=./wheels -r requirements.txt
```

---

## ⚙️ Configuration & Environment Variables

Copy the sample environment file:
```bash
cp .env.example .env
```

Edit `.env` using your preferred text editor:

```ini
# ==============================================================================
# USTAAD-IN-A-BOX ENVIRONMENT CONFIGURATION
# ==============================================================================

# Server Network Binding
PORT=8000
HOST=0.0.0.0

# Deterministic Engine Settings
RULES_FILE=rules.yaml
SYNONYMS_FILE=synonyms.yaml
LOGS_FILE=interactions.jsonl

# Groq Cloud API Configuration (Leave blank for 100% offline mode)
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=qwen/qwen3.8-27b
GROQ_WHISPER_MODEL=whisper-large-v3-turbo

# Local STT Settings (Fallback / Offline)
WHISPER_LOCAL_MODEL=base
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=int8
```

---

## 🚀 Running the Server

### Interactive Development Run
```bash
python main.py
```
Output will confirm:
```
============================================================
  Ustaad-in-a-Box — FastAPI Server
============================================================
  Server running at: http://0.0.0.0:8000
  Rules loaded:      16 rules from rules.yaml
  Groq LLM Phraser:  ENABLED (model: qwen/qwen3.8-27b)
  Whisper STT:       DUAL (Cloud Groq Whisper + Local fallback)
============================================================
```

### Windows One-Click Batch Script
Double-click `run.bat` or run:
```cmd
run.bat
```

---

## 🐧 Production Linux Systemd Daemon Service

To ensure Ustaad-in-a-Box boots automatically when the salvaged laptop powers on:

1. Create a systemd service file:
```bash
sudo nano /etc/systemd/system/ustaad.service
```

2. Paste the following configuration:
```ini
[Unit]
Description=Ustaad-in-a-Box Phone Repair Stand-In
After=network.target sound.target

[Service]
Type=simple
User=repairbot
WorkingDirectory=/home/repairbot/Ustaad-In-A-Box
ExecStart=/home/repairbot/Ustaad-In-A-Box/venv/bin/python main.py
Restart=always
RestartSec=3
EnvironmentFile=/home/repairbot/Ustaad-In-A-Box/.env
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ustaad.service
sudo systemctl start ustaad.service
sudo systemctl status ustaad.service
```

---

## 🔒 Kiosk Mode Configuration (For Competition Booth Displays)

To lock down the exhibition laptop into a dedicated kiosk terminal:

### On Chromium / Google Chrome:
```bash
google-chrome --kiosk --incognito --disable-pinch --overscroll-history-navigation=0 http://127.0.0.1:8000/
```

### On Windows Edge Kiosk:
```cmd
start msedge --kiosk http://127.0.0.1:8000/ --edge-kiosk-type=fullscreen
```

---

## 🛠️ Troubleshooting & Diagnostic Runbook

### Issue 1: Microphone Not Recording in Browser
- **Cause**: Modern browsers restrict `navigator.mediaDevices.getUserMedia` on insecure HTTP connections.
- **Solution**: Access the UI via `http://localhost:8000` or `http://127.0.0.1:8000` (which browsers treat as secure origins). If accessing across a local LAN, configure self-signed SSL or reverse-proxy with Caddy/Nginx.

### Issue 2: Local Whisper Takes Too Long on Ancient CPU
- **Cause**: Core 2 Duo lacks AVX2 instruction sets.
- **Solution**:
  1. Set `WHISPER_LOCAL_MODEL=tiny` in `.env`.
  2. Ensure `WHISPER_COMPUTE_TYPE=int8` is active.
  3. Reduce microphone recording chunk duration to < 4 seconds.

### Issue 3: Groq API Key Limit or Network Timeout
- **Symptom**: Server console logs `Groq API timeout (>4s)`.
- **Behavior**: The system gracefully falls back to the deterministic canonical rule text in 0 ms.
- **Verification**: Check the frontend answer card — the canonical rule text will display directly, and the telemetry sidebar will report `Generation Layer: Deterministic Rule Engine`.

---

## 📊 Backup & Data Audit Maintenance

The append-only log is written to `interactions.jsonl`. To rotate or back up logs:

```bash
# Export CSV snapshot:
curl -s http://127.0.0.1:8000/api/logs/export > backup_$(date +%Y%m%d).csv

# Check live statistics:
curl -s http://127.0.0.1:8000/api/stats | python -m json.tool
```
