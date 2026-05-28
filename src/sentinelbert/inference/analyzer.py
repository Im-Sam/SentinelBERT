from pathlib import Path
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)


class LogAnalyzer:
    def __init__(self, model_path=None):

        # -------------------------------------------------
        # Resolve project root
        # -------------------------------------------------
        ROOT = Path(__file__).resolve().parents[3]

        # -------------------------------------------------
        # Correct global model location
        # -------------------------------------------------
        if model_path is None:
            model_path = ROOT / "models" / "save_model"

        model_path = Path(model_path).resolve()

        print(f"Loading model from: {model_path}")

        # -------------------------------------------------
        # Load tokenizer + model locally
        # -------------------------------------------------
        self.tokenizer = AutoTokenizer.from_pretrained(
            str(model_path),
            local_files_only=True
        )

        self.model = AutoModelForSequenceClassification.from_pretrained(
            str(model_path),
            local_files_only=True
        )

        self.model.eval()

    def predict(self, log_line):

        inputs = self.tokenizer(
            log_line,
            return_tensors="pt",
            truncation=True,
            padding=True
        )

        with torch.no_grad():
            outputs = self.model(**inputs)

        probs = torch.softmax(outputs.logits, dim=1)

        anomaly_score = probs[0][1].item()

        if anomaly_score > 0.8:
            risk = "HIGH"
        elif anomaly_score > 0.4:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        return {
            "log": log_line,
            "anomaly_score": round(anomaly_score, 4),
            "risk": risk
        }