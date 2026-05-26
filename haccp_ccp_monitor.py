#%%
#!/usr/bin/env python3
"""
Tool ID: QA-T02 | Framework: ISO 22000:2018 Clause 8.5.2 / HACCP
Description: Automated CCP validation loop analyzing thermal telemetry logs.
Verifies compliance with KEBS/EAS critical limits (e.g., pasteurization/holding targets).
"""

import datetime
import json
import math
import sys


class HACCPCCPMonitor:

    def __init__(self, reference_temp_c=72.0, z_value_c=10.0, target_f0_seconds=15.0):
        """
        Initializes the kinetic calculation matrix.
        Default baseline parameters reflect high-temperature short-time (HTST) pasteurization:
        72.0°C reference hold for a minimum of 15 contiguous seconds.
        """
        self.reference_temp = reference_temp_c
        self.z_value = z_value_c
        self.target_f0_minutes = target_f0_seconds / 60.0

    def parse_telemetry_stream(self, data_stream_json):
        """
        Parses real-time or batched JSON data packages from pipeline temperature logs.
        Expected format: {'timestamp': ISO_string, 'temperature_c': float, 'sensor_id': string}
        """
        try:
            payload = json.loads(data_stream_json)
            return {
                "timestamp": datetime.datetime.fromisoformat(payload["timestamp"]),
                "temp_c": float(payload["temperature_c"]),
                "sensor_id": str(payload["sensor_id"]),
            }
        except (ValueError, KeyError) as error_msg:
            print(
                f"[SYSTEM ERROR] Failed parsing incoming log packet: {error_msg}",
                file=sys.stderr,
            )
            return None

    def evaluate_thermal_batch(self, time_series, temp_series):
        """
        Executes numerical trapezoidal integration across data arrays to compute
        the integrated cumulative lethal value (F0 equivalent minutes).
        F0 = integral( 10^((T - T_ref) / z) * dt )
        """
        if len(time_series) != len(temp_series) or len(time_series) < 2:
            raise ValueError(
                "Data dimension mismatch: Series lengths must be identical and contain >= 2 entries."
            )

        total_f0_accumulated = 0.0
        lethal_rates = [
            10 ** ((t - self.reference_temp) / self.z_value) for t in temp_series
        ]

        # Numerical integration loop over time points
        for idx in range(len(time_series) - 1):
            # Calculate time delta in fractional minutes
            delta_t_sec = (time_series[idx + 1] - time_series[idx]).total_seconds()
            delta_t_min = delta_t_sec / 60.0

            # Midpoint trapezoidal approximation for lethal velocity acceleration
            mean_lethal_rate = (lethal_rates[idx] + lethal_rates[idx + 1]) / 2.0
            total_f0_accumulated += mean_lethal_rate * delta_t_min

        # CCP validation checks
        target_met = total_f0_accumulated >= self.target_f0_minutes

        if target_met:
            compliance_status = "PASSED - CCP VALIDATED"
            corrective_action = "None. Batch exhibits structural micro-organism target reduction."
        else:
            compliance_status = "CRITICAL LIMIT BREACH DETECTED"
            corrective_action = "QUARANTINE LOT IMMEDIATELY. Divert output line to recirculate. Check pasteurizer steam flow pressure."

        return {
            "accumulated_f0_minutes": round(total_f0_accumulated, 5),
            "required_f0_minutes": round(self.target_f0_minutes, 5),
            "status": compliance_status,
            "corrective_action_pathway": corrective_action,
        }


# --- Active Field Execution Test ---
if __name__ == "__main__":
    print("=====================================================================")
    print("       INITIALIZING HACCP CCP TELEMETRY PARSING SYSTEM               ")
    print("=====================================================================\n")

    # Initialize monitor instance
    monitor = HACCPCCPMonitor(
        reference_temp_c=72.0, z_value_c=10.0, target_f0_seconds=15.0
    )

    # Simulating a data stream from an in-line pasteurization temperature sensor
    base_time = datetime.datetime.now()
    raw_packets = [
        {"timestamp": base_time.isoformat(), "temperature_c": 68.5, "sensor_id": "CCP-T1"},
        {"timestamp": (base_time + datetime.timedelta(seconds=5)).isoformat(), "temperature_c": 72.4, "sensor_id": "CCP-T1"},
        {"timestamp": (base_time + datetime.timedelta(seconds=10)).isoformat(), "temperature_c": 72.8, "sensor_id": "CCP-T1"},
        {"timestamp": (base_time + datetime.timedelta(seconds=15)).isoformat(), "temperature_c": 72.1, "sensor_id": "CCP-T1"},
        {"timestamp": (base_time + datetime.timedelta(seconds=20)).isoformat(), "temperature_c": 64.0, "sensor_id": "CCP-T1"},
    ]

    # Process logs into system arrays
    parsed_times = []
    parsed_temps = []

    for packet in raw_packets:
        json_str = json.dumps(packet)
        parsed = monitor.parse_telemetry_stream(json_str)
        if parsed:
            parsed_times.append(parsed["timestamp"])
            parsed_temps.append(parsed["temp_c"])

    # Run analytical verification evaluation
    batch_analysis = monitor.evaluate_thermal_batch(parsed_times, parsed_temps)

    print(f"Sensor Evaluation Target: {raw_packets[0]['sensor_id']}")
    print(f"Calculated Lethality Index (F0): {batch_analysis['accumulated_f0_minutes']} equiv. minutes")
    print(f"Minimum Process Threshold Target: {batch_analysis['required_f0_minutes']} equiv. minutes")
    print(f"Verification Output Verdict     : [{batch_analysis['status']}]")
    print(f"Directive Action Requirements   : {batch_analysis['corrective_action_pathway']}")
    print("\n=====================================================================")



=====================================================================
       INITIALIZING HACCP CCP TELEMETRY PARSING SYSTEM               
=====================================================================

Sensor Evaluation Target: CCP-T1
Calculated Lethality Index (F0): 0.30205 equiv. minutes
Minimum Process Threshold Target: 0.25 equiv. minutes
Verification Output Verdict     : [PASSED - CCP VALIDATED]
Directive Action Requirements   : None. Batch exhibits structural micro-organism target reduction.

=====================================================================
