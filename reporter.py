import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment.")

client = Groq(api_key=api_key)

# Pick an active model dynamically from your account
try:
    available_models = [m.id for m in client.models.list().data]
    # Prioritize general chat models
    preferred = [m for m in available_models if "preview" not in m and "whisper" not in m]
    ACTIVE_MODEL = preferred[0] if preferred else available_models[0]
except Exception:
    ACTIVE_MODEL = "gemma2-9b-it"

print(f"Using Groq model: {ACTIVE_MODEL}")

def generate_report(anomalies: list[dict]) -> str:
    if not anomalies:
        return "No spending anomalies detected above the defined thresholds."

    system_instruction = """
You are a Cloud FinOps Engineer. Analyze the given list of cloud cost anomalies.
Produce a clean Markdown report structured as:
1. Executive Impact (Total unexpected daily burn, monthly projection)
2. Breakdown per Service:
   - Identify common architectural culprits for that specific service
   - 2-3 immediate CLI or Console remediation steps
   - Long-term prevention tip (e.g., IaC drift, alerts)
Keep the tone concise, authoritative, and actionable.
"""

    prompt = f"Cost Anomalies Data:\n{json.dumps(anomalies, indent=2)}"

    chat_completion = client.chat.completions.create(
        model=ACTIVE_MODEL,
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    return chat_completion.choices[0].message.content
