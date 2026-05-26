# Food Safety Quality Assurance Tools (`food-safety-qa-tools`)

[![Compliance](https://img.shields.io/badge/Compliance-KEBS%20%7C%20ISO%2022000-blue.svg)](https://www.kebs.org)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)
[![R-Lang](https://img.shields.io/badge/R--Lang-4.0%2B-orange.svg)](https://www.r-project.org/)

An enterprise-grade repository containing analytical scripts, dynamic audit tools, and programmatic documentation for Quality Assurance (QA) pipelines across industrial microbiology, food manufacturing, and mycotoxin hazard mitigation. 

This toolkit bridges the gap between field telemetry data and national/international compliance boundaries—specifically optimized for **East African Standards (EAS)**, the **Kenya Bureau of Standards (KEBS)** thresholds, and **ISO 22000:2018** food safety management frameworks.

---

## Core Framework & Study Mapping

The tools in this repository are modeled directly on empirical food safety data and localized vulnerability metrics identified across recent Kenyan value-chain surveillance studies:

* **Mycotoxin Proliferation Tracking**: Engineered to target the strict **< 10 ppb** total aflatoxin regulatory limit enforced by KEBS, addressing high-risk storage vulnerabilities observed in regional grain silos (e.g., Kiambu County milling hubs).
* **Microbial Kinetic Assessment**: Automates $D\text{-value}$ and $z\text{-value}$ mathematical integration to verify thermal sterilization lines, grounded in processing plant contamination vector profiles (e.g., Homa Bay puree lines).
* **Value-Chain Hygiene Auditing**: Dynamic scorecards evaluating retail and SME processing sanitation indicators against a historical baseline average of **58%** compliance.

---

## Repository Architecture & Tool Inventory

```text
├── drivers/
│   ├── aflatoxin_risk_predict.py     # Predicts Aspergillus flavus risk indices
│   ├── haccp_ccp_monitor.py          # Real-time F0-value thermal log integration
│   ├── coliform_cfu_calculator.py    # Standardizes plate-count serial dilution math
│   └── water_potability_monitor.py   # Processes multi-point fecal coliform assays
├── checklists/
│   └── prp_audit_checklist.xlsx      # Interactive ISO 22000/GMP audit dashboard
├── requirements.txt                  # Python dependencies
└── README.md                         # Project documentation
