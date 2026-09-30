import os
import requests

def send_alert(markdown_report: str):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL") or os.getenv("DISCORD_WEBHOOK_URL")

    if not webhook_url:
        print("[!] No SLACK_WEBHOOK_URL or DISCORD_WEBHOOK_URL configured. Skipping chat delivery.")
        return

    # Formatting payload for Slack or Discord
    is_discord = "discord.com" in webhook_url

    if is_discord:
        # Discord has a 2000 character cap per message
        payload = {
            "content": f"🚨 **FinOps Anomaly Alert Detected**\n\n{markdown_report[:1850]}..."
        }
    else:
        # Slack payload
        payload = {
            "text": f"🚨 *FinOps Anomaly Alert Detected*\n\n{markdown_report[:2900]}"
        }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code in (200, 204):
            print("[+] Notification delivered to chat channel.")
        else:
            print(f"[!] Webhook returned HTTP {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[!] Notification error: {e}")
