# AI FinOps Cloud Cost Anomaly Inspector

An automated cloud cost intelligence agent that ingests AWS spending metrics, performs statistical anomaly detection using rolling baseline Z-scores, and generates executive FinOps remediation briefs using LLM inference via Groq.

## Architecture
## Features

- **Automated Ingestion**: Queries 30-day multi-service usage data via `boto3` (`ce:GetCostAndUsage`).
- **Statistical Detection**: Evaluates rolling standard deviations ($Z \ge 2.0$, $\Delta \ge \$5.00$) to eliminate false alerts.
- **LLM-Powered Remediation**: Generates instant triage checklists, CLI commands, and architectural root cause analyses.
- **Automated CI/CD Execution**: Runs serverless audits daily at 08:00 UTC via GitHub Actions.
- **Simulation Mode**: Built-in `--simulate` switch to test pipelines against synthetic cloud spikes.

## Local Setup

1. **Clone & Install Dependencies**:
   ```bash
   git clone [https://github.com/Akshit0010/finops-anomaly-inspector.git](https://github.com/Akshit0010/finops-anomaly-inspector.git)
   cd finops-anomaly-inspector
   pip install -r requirements.txt
Environment Variables:
Create a .env file:

Code snippet
GROQ_API_KEY="your-groq-key"
AWS_ACCESS_KEY_ID="your-aws-access-key"
AWS_SECRET_ACCESS_KEY="your-aws-secret-key"
AWS_DEFAULT_REGION="us-east-1"
SLACK_WEBHOOK_URL="optional-webhook-url"
Run Audit:

Bash
# Live account scan
python main.py

# Test with injected synthetic spikes
python main.py --simulate
