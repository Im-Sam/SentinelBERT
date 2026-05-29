import pandas as pd
import random
from datetime import datetime, timedelta

VM_NAMES = ["vm-web-01", "vm-db-02", "vm-ad-01", "vm-linux-03"]
EVENTS = ["Sign-in success", "Sign-in failed", "Token issued", "MFA challenge"]

def generate_azure_log(anomaly=False):
    vm = random.choice(VM_NAMES)
    event = random.choice(EVENTS)

    ip = "10.0.0." + str(random.randint(1, 255))

    if anomaly:
        ip = f"185.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        event = "FAILED SIGN-IN BRUTE FORCE"

    timestamp = datetime.now() - timedelta(minutes=random.randint(1, 10000))

    return {
        "timestamp": timestamp,
        "vm": vm,
        "event": event,
        "ip": ip,
        "anomaly": int(anomaly)
    }

def create(n=1000):
    data = []

    for _ in range(n):
        anomaly = random.random() < 0.2
        data.append(generate_azure_log(anomaly))

    df = pd.DataFrame(data)
    df.to_csv("data/azure_vm_logs.csv", index=False)
    print("Azure VM dataset generated")

if __name__ == "__main__":
    create()