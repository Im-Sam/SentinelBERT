import os
import pandas as pd
import numpy as np

from datasets import Dataset
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments,
    DataCollatorWithPadding
)
from sklearn.model_selection import train_test_split

MODEL_NAME = "distilbert-base-uncased"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "save_model")

# ----------------------------
# Load datasets
# ----------------------------
def load_data():
    synthetic_path = os.path.join(BASE_DIR, "../data/synthetic_logs.csv")
    azure_path = os.path.join(BASE_DIR, "../data/azure_vm_logs.csv")

    df1 = pd.read_csv(synthetic_path)
    df2 = pd.read_csv(azure_path)

    # Azure dataset has different schema → convert to log format
    df2["log"] = (
        df2["timestamp"].astype(str) +
        " VM=" + df2["vm"].astype(str) +
        " EVENT=" + df2["event"].astype(str) +
        " IP=" + df2["ip"].astype(str)
    )

    # Ensure both have same schema
    df1 = df1[["log", "label"]]
    df2 = df2[["log", "anomaly"]].rename(columns={"anomaly": "label"})

    df = pd.concat([df1, df2], ignore_index=True)

    return df


# ----------------------------
# Tokenization
# ----------------------------
def tokenize(batch, tokenizer):
    return tokenizer(batch["log"], truncation=True)


def main():
    print("Loading datasets...")

    df = load_data()

    print(f"Dataset size: {len(df)}")

    X = df["log"].to_numpy()
    y = df["label"].to_numpy()

    train_texts, val_texts, train_labels, val_labels = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y if len(np.unique(y)) > 1 else None
    )

    train_dataset = Dataset.from_dict({
        "log": train_texts,
        "label": train_labels
    })

    val_dataset = Dataset.from_dict({
        "log": val_texts,
        "label": val_labels
    })

    print("Loading tokenizer...")
    tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_NAME)

    train_dataset = train_dataset.map(lambda x: tokenize(x, tokenizer), batched=True)
    val_dataset = val_dataset.map(lambda x: tokenize(x, tokenizer), batched=True)

    train_dataset = train_dataset.rename_column("label", "labels")
    val_dataset = val_dataset.rename_column("label", "labels")

    train_dataset.set_format("torch")
    val_dataset.set_format("torch")

    print("Loading model...")
    model = DistilBertForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2
    )

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    # ----------------------------
    # Training args (IMPORTANT FIX)
    # ----------------------------
    training_args = TrainingArguments(
        output_dir=SAVE_DIR,
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
        logging_dir=os.path.join(SAVE_DIR, "logs"),
        logging_steps=10,
        load_best_model_at_end=True,
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator
    )

    print("Starting training...")
    trainer.train()

    # ----------------------------
    # FORCE SAVE (this fixes your issue)
    # ----------------------------
    print("Saving model...")

    os.makedirs(SAVE_DIR, exist_ok=True)

    trainer.save_model(SAVE_DIR)
    tokenizer.save_pretrained(SAVE_DIR)

    print(f"Model saved to: {SAVE_DIR}")


if __name__ == "__main__":
    main()