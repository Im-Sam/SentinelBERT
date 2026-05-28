import sys
import os
import streamlit as st
import pandas as pd
from pathlib import Path

# -------------------------------------------------
# FIX: ensure project root is on sys.path FIRST
# -------------------------------------------------
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from sentinelbert.inference.analyzer import LogAnalyzer

st.title("SentinelBERT — Log Anomaly Detector")

MODEL_PATH = ROOT / "models" / "save_model"
MODEL_PATH = MODEL_PATH.resolve()
analyzer = LogAnalyzer(str(MODEL_PATH))

uploaded_file = st.file_uploader("Upload log CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    results = []

    for log in df["log"]:
        pred = analyzer.predict(log)
        results.append(pred)

    results_df = pd.DataFrame(results)

    st.dataframe(results_df)

    st.bar_chart(results_df["anomaly_score"])