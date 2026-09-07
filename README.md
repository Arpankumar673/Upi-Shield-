# UPI-Shield 🛡️
> **Contextual Digital Payment Scam & Coercion Detector**  
> *Career Catalyst Club × GeeksforGeeks Hackathon (CC-GFG-02)*

UPI-Shield is a contextual digital payment scam and coercion detection system. It analyzes suspicious SMS, WhatsApp, and payment-related messages, identifies deceptive or coercive signals (urgency, threats, authority impersonation, payment pressure, credential requests, reward manipulation), calculates a normalized risk score (0–100), explains the risk factors, and provides bilingual English/Hindi safety guidance.

---

## 🏗️ Project Architecture & Modular Design

```text
upi-shield/
├── app.py                     # Streamlit User Interface Shell
├── requirements.txt           # Python Dependencies
├── .env.example               # Environment Configuration Template
├── README.md                  # Project Documentation
├── docs/                      # Specification & Hackathon Documentation
├── data/
│   └── sample_messages.py     # Preloaded Safe & Scam Test Cases
├── src/
│   ├── config.py              # Risk Scoring Weights & Thresholds Configuration
│   ├── preprocessing/         # Text Normalization & Extraction
│   ├── detection/             # Deception & Coercion Signal Engine
│   ├── scoring/               # Risk Scoring & Level Aggregation Engine
│   ├── explanations/          # Explainability & Evidence Generator
│   ├── guidance/               # English & Hindi Safety Guidance Generator
│   ├── ocr/                   # Image OCR Handler (Bonus / Modular)
│   └── upi/                   # UPI Intent URI Parser (Bonus / Modular)
└── tests/
    └── test_smoke.py          # Automated Modular Smoke Tests
```

---

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Create Python virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell / CMD):
.\.venv\Scripts\activate

# macOS / Linux:
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Streamlit Application
```bash
streamlit run app.py
```

### 4. Run Smoke Tests
```bash
pytest tests/
```

---

## 🎯 Phase 1 MVP Scope
- Clean, modular Python project structure.
- Initial Streamlit UI Shell with preloaded sample messages.
- Clear separation of concerns (UI, preprocessing, detection, scoring, explanations, bilingual guidance).
- Deterministic core detection architecture (no black-box or external API dependency for basic flow).
- Built-in English and Hindi safety advice structure.

---

## 📜 License
Developed for CC-GFG-02 Hackathon.
