#!/usr/bin/env python3
"""
Tool ID: QA-T01 | Framework: HACCP / Codex Alimentarius
Function: Automated predictive risk calculations for Aspergillus flavus 
          and mycotoxin accumulation in stored maize grains.
Customized for: KEBS Regulatory Action Limit (< 10 ppb total Aflatoxin)
"""

import math

def calculate_aflatoxin_risk(temp_c, relative_humidity_pct, storage_days, grain_moisture_pct):
    """
    Computes an empirical Aflatoxin Proliferation Risk Index (APRI).
    Optimized for East African storage profiles (Kiambu/Eastern regions).
    """
    # 1. Evaluate baseline biological growth boundaries for Aspergillus flavus
    if temp_c < 12 or temp_c > 48:
        temperature_factor = 0.05
    else:
        # Peak kinetic optimization between 28°C and 37°C
        temperature_factor = math.exp(-0.5 * ((temp_c - 33.0) / 7.0) ** 2)
        
    # 2. Grain equilibrium moisture content hazard evaluation
    if grain_moisture_pct > 13.5:  # KEBS dry target limit is 13.5% max
        moisture_multiplier = 1.8 * (grain_moisture_pct - 13.5)
    else:
        moisture_multiplier = 0.1
        
    # 3. Relative Humidity kinetic acceleration factor
    if relative_humidity_pct > 70:
        rh_factor = ((relative_humidity_pct - 70) / 30) ** 2
    else:
        rh_factor = 0.02

    # 4. Compounding temporal mathematical matrix
    raw_index = (temperature_factor * moisture_multiplier * (1 + rh_factor)) * storage_days
    risk_index = min(100.0, max(0.0, raw_index * 10))
    
    # 5. Map to localized regulatory action pathways
    if risk_index >= 65.0 or grain_moisture_pct > 15.0:
        status = "CRITICAL VIOLATION WARNING"
        action = "Immediate aeration/mechanical drying needed. Predicted to breach 10ppb KEBS threshold."
    elif 35.0 <= risk_index < 65.0:
        status = "ALERT - ELEVATED HAZARD"
        action = "Increase sampling frequency. Audit airtight seal integrity of hermetic storage units."
    else:
        status = "COMPLIANT / SAFE"
        action = "Maintain continuous temperature & humidity data logging."
        
    return {
        "apri_score": round(risk_index, 2),
        "status": status,
        "action_required": action
    }

# --- Quick Validation Run ---
if __name__ == "__main__":
    print("[Testing Run]: High-moisture storage batch mimicking poor drying conditions:")
    result = calculate_aflatoxin_risk(temp_c=29.5, relative_humidity_pct=78.2, storage_days=14, grain_moisture_pct=16.2)
    print(f"Calculated Index: {result['apri_score']}\nStatus: {result['status']}\nAction: {result['action_required']}\n")
