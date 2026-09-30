import pandas as pd
import numpy as np

def detect_anomalies(df: pd.DataFrame, z_threshold: float = 2.0, min_dollar_spike: float = 5.0) -> list[dict]:
    """
    Evaluates rolling historical baselines.
    Flags an anomaly if:
      - Z-Score >= z_threshold
      - Spend delta >= min_dollar_spike
    """
    anomalies = []
    if df.empty:
        return anomalies

    for service, group in df.groupby("service"):
        group = group.sort_values("date")
        if len(group) < 5:
            continue
            
        history = group.iloc[:-1]["cost"]
        mean_cost = history.mean()
        std_cost = history.std()
        
        latest_row = group.iloc[-1]
        latest_cost = latest_row["cost"]
        dollar_spike = latest_cost - mean_cost
        
        z_score = 0.0 if (std_cost == 0 or np.isnan(std_cost)) else (dollar_spike / std_cost)
        
        if z_score >= z_threshold and dollar_spike >= min_dollar_spike:
            anomalies.append({
                "service": service,
                "date": latest_row["date"].strftime("%Y-%m-%d"),
                "latest_cost": round(latest_cost, 2),
                "baseline_mean": round(mean_cost, 2),
                "dollar_spike": round(dollar_spike, 2),
                "z_score": round(z_score, 2)
            })
            
    return anomalies
