from datasets import Dataset
import pandas as pd

def load_dataset(path="data/synthetic_logs.csv"):
    df = pd.read_csv(path)
    return Dataset.from_pandas(df)