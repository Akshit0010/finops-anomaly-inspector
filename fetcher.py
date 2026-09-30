import boto3
from datetime import datetime, timedelta
import pandas as pd

def fetch_daily_costs(days_back: int = 30) -> pd.DataFrame:
    """
    Pulls daily unblended costs grouped by service from AWS Cost Explorer.
    Requires IAM permission: ce:GetCostAndUsage
    """
    client = boto3.client("ce", region_name="us-east-1")
    
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days_back)
    
    response = client.get_cost_and_usage(
        TimePeriod={
            "Start": start_date.strftime("%Y-%m-%d"),
            "End": end_date.strftime("%Y-%m-%d")
        },
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}]
    )
    
    records = []
    for day in response.get("ResultsByTime", []):
        date_str = day["TimePeriod"]["Start"]
        for group in day.get("Groups", []):
            service_name = group["Keys"][0]
            amount = float(group["Metrics"]["UnblendedCost"]["Amount"])
            records.append({
                "date": pd.to_datetime(date_str),
                "service": service_name,
                "cost": amount
            })
            
    return pd.DataFrame(records)
