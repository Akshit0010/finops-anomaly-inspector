from reporter import generate_report

# Mock anomaly data simulating a spike
sample_anomalies = [
    {
        "service": "Amazon EC2-Other (NAT Gateway)",
        "date": "2026-09-29",
        "latest_cost": 312.40,
        "baseline_mean": 38.10,
        "dollar_spike": 274.30,
        "z_score": 4.12
    },
    {
        "service": "Amazon DynamoDB",
        "date": "2026-09-29",
        "latest_cost": 89.00,
        "baseline_mean": 12.50,
        "dollar_spike": 76.50,
        "z_score": 3.05
    }
]

print("Sending data to Gemini...")
report = generate_report(sample_anomalies)
print("\n" + "=" * 60)
print(report)
print("=" * 60)