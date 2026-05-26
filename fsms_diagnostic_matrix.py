#%%
#!/usr/bin/env python3
"""
Tool ID: QA-T05 | Framework: ISO 22000:2018 / FSMS Diagnostic Framework
Function: Systemic Operational Vulnerability Diagnostic Model
"""

class FSMSDiagnosticMatrix:
    def __init__(self, facility_name):
        self.facility_name = facility_name
        self.diagnostic_scores = {}

    def grade_core_dimensions(self, context_score, control_activities, assurance_activities):
        """
        Calculates organizational capability level (Scale 1 to 3).
        Based on international diagnostic models for developing market SMEs.
        """
        # Context Score: 1 (High Risk Environment) to 3 (Highly Structured Internal Layout)
        # Control Activities: 1 (Reactive Controls) to 3 (Proactive Automated Interventions)
        # Assurance Activities: 1 (Basic Testing) to 3 (Validated Traceability Systems)
        
        self.diagnostic_scores['Contextual_Risk'] = context_score
        self.diagnostic_scores['Control_Execution'] = control_activities
        self.diagnostic_scores['Assurance_Validation'] = assurance_activities
        
        systemic_index = (context_score + control_activities + assurance_activities) / 3.0
        
        if systemic_index < 1.7:
            tier = "LEVEL 1 - BASIC / REACTIVE SYSTEM"
            outlook = "High risk of systematic escape. Over-reliance on end-product sorting. Needs foundational PRP re-engineering."
        elif 1.7 <= systemic_index < 2.5:
            tier = "LEVEL 2 - STANDARD SYSTEM"
            outlook = "HACCP structure functional, but lacks advanced predictive verification tools. Susceptible to variable ingredient shifts."
        else:
            tier = "LEVEL 3 - ADVANCED PROACTIVE FSMS"
            outlook = "Excellent validation framework. Systems completely integrated into continuous telemetry loops."
            
        return {
            "computed_index": round(systemic_index, 2),
            "maturity_tier": tier,
            "systemic_outlook": outlook
        }

# --- Execute System Assessment Run ---
evaluator = FSMSDiagnosticMatrix("Nairobi SME Beverage Processor Alpha")
assessment = evaluator.grade_core_dimensions(context_score=2, control_activities=1, assurance_activities=2)
print(f"Facility Profile: {evaluator.facility_name}\nIndex Score: {assessment['computed_index']}\nMaturity Tier: {assessment['maturity_tier']}\nOutlook Report: {assessment['systemic_outlook']}")
