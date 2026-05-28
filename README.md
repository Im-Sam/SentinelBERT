# 🧠 SentinelBERT — AI Log Anomaly Detector

SentinelBERT is a transformer-based anomaly detection system for Windows and Azure authentication logs.

It fine-tunes a DistilBERT model to classify log lines as **normal or suspicious**, enabling early detection of credential abuse, brute force attempts, and anomalous authentication behavior.

---

# 🚨 System Overview

SentinelBERT is built as a full pipeline:

1. **Generate synthetic security logs (Windows + Azure VM)**
2. **Train a transformer model on labeled log data**
3. **Run inference on raw logs**
4. **Visualize anomalies in a SOC-style dashboard**

---

# 🏗️ BUILD PIPELINE (IMPORTANT)

Follow this exact order to reproduce the system:

## Setup
### Create venv
>python -m venv venv

### Activate:

Windows

>venv\Scripts\activate

Mac/Linux

>source venv/bin/activate

### Install Dependencies (BUILD REQUIREMENT)

>pip install -r requirements.txt
>pip install "transformers[torch]" accelerate

### Generate Training Data (CRITICAL BUILD STEP)

You MUST generate logs before training.

**Windows / SIEM-style logs**
>python data/generate_logs.py

Output:

data/synthetic_logs.csv

**Azure VM / AD-style logs**
>python data/azure_vm_logs.py

Output:

data/azure_vm_logs.csv

### Train the Model (CORE BUILD STEP)
>python -m src.sentinelbert.model.train

What happens here:

- Loads synthetic_logs.csv
- Tokenizes log strings using DistilBERT tokenizer
- Fine-tunes transformer classifier
- Evaluates on holdout set
- Saves model artifacts

Output model path:

models/save_model/

This folder contains:

- trained model weights
- tokenizer config
- label mappings

### VERIFY MODEL (OPTIONAL BUT RECOMMENDED)

Run CLI inference:
> python -m src.sentinelbert.inference.predict

Paste a log line like:

>2026-05-28 EventID=4625 User=admin IP=185.22.11.9 Status=FAIL

Expected output:

```
{
  "log": "2026-05-28 EventID=4625 User=admin IP=185.22.11.9 Status=FAIL",
  "anomaly_score": 0.9997,
  "risk": "HIGH"
}
```

### RUN SOC DASHBOARD (DEPLOYMENT STEP)
streamlit run src/sentinelbert/app/streamlit.py

Then open:

http://localhost:8501