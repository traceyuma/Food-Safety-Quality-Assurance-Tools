#%%
#!/usr/bin/env python3
"""
Tool ID: QA-T03 | Framework: KEBS / East African Standards (EAS)
Function: Plate-count tracking automation & regulatory maximum tolerance boundary flagging.
Target: E. coli and total coliform density limits in food matrices.
"""

def evaluate_microbial_load(colony_count, dilution_factor, sample_volume_ml=1.0):
    """
    Calculates Colony Forming Units per gram/ml (CFU/g or CFU/ml).
    Evaluates against KEBS standard tolerances (< 100 CFU/g for raw meat/poultry retail units).
    """
    # Handle standard laboratory microbial countable range restrictions (30 - 300 CFU rule)
    if colony_count == 0:
        cfu_result = 0.0
        flag = "ABSENT - CONFORMS"
    else:
        cfu_result = (float(colony_count) * (10 ** dilution_factor)) / sample_volume_ml

        # KEBS standard limit for critical hygiene indicators (E. coli)
        if cfu_result > 100.0:
            flag = "REJECT - EXCEEDS REGULATORY MAXIMUM CEILING"
        elif 50.0 <= cfu_result <= 100.0:
            flag = "MARGINAL COMPLIANCE WARNING"
        else:
            flag = "PASS - ACCEPTS MARKET LEVEL"

    return {
        "calculated_cfu": cfu_result,
        "formatted_scientific": f"{cfu_result:.2e}",
        "regulatory_status": flag
    }

# --- Quick Validation Run ---
if __name__ == "__main__":
    print("[Testing Run]: High load detection sample:")
    assay_test = evaluate_microbial_load(colony_count=142, dilution_factor=1)
    print(f"Microbial Load: {assay_test['calculated_cfu']} CFU/g | Status: {assay_test['regulatory_status']}") 
  
