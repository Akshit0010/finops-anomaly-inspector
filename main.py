import sys
import pandas as pd
from fetcher import fetch_daily_costs
from detector import detect_anomalies
from reporter import generate_report

def run_inspector(simulate: bool = False):
    print("[1/3] Querying AWS Cost Explorer (past 30 days)...")
    try:
        df = fetch_daily_costs(days_back=30)
    except Exception as e:
        print(f"\n[!] AWS Error: {e}")
        return

    if simulate:
        print("\n[i] Simulation Mode: Injecting synthetic NAT Gateway & RDS anomalies...")
        synthetic_spikes = pd.DataFrame([
            {
                "date": pd.to_datetime("today"),
                "service": "Amazon EC2-Other",
                "cost": 184.20
            },
            {
                "date": pd.to_datetime("today"),
                "service": "Amazon Relational Database Service",
                "cost": 94.50
            }
        ])
        df = pd.concat([df, synthetic_spikes], ignore_index=True)

    print(f"[2/3] Analyzing spend across {df['service'].nunique()} services...")
    anomalies = detect_anomalies(df, z_threshold=2.0, min_dollar_spike=5.0)

    if not anomalies:
        print("No active spending anomalies found above thresholds.")
        return

    print(f"Detected {len(anomalies)} spending anomaly/anomalies.")
    print("[3/3] Generating FinOps remediation report via Groq...")
    report = generate_report(anomalies)

    report_file = "finops_report.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    # Send to Slack/Discord if configured
    send_alert(report)  

    print("\n" + "=" * 60)
    print(report)
    print("=" * 60)
    print(f"\nReport saved to {report_file}")

if __name__ == "__main__":
    simulate_flag = "--simulate" in sys.argv
    run_inspector(simulate=simulate_flag)