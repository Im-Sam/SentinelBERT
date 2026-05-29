import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

EVENT_IDS = ["4625", "4768", "4769"]  # auth failures / ticketing events
IP_POOL = ["10.0.0.5", "10.0.0.8", "192.168.1.10", "172.16.0.2"]

def generate_log(anomaly=False):
    timestamp = datetime.now() - timedelta(minutes=random.randint(1, 5000))
    
    ip = random.choice(IP_POOL)
    user = fake.user_name()
    event_id = random.choice(EVENT_IDS)

    if anomaly:
        ip = fake.ipv4()  # external suspicious IP
        user = user + str(random.randint(1000, 9999))

    log = f"{timestamp} EventID={event_id} User={user} IP={ip} Status={'FAIL' if anomaly else 'SUCCESS'}"
    
    return log, int(anomaly)

def create_dataset(n=2000):
    logs = []
    labels = []

    for _ in range(n):
        anomaly = random.random() < 0.25  # 25% anomalies
        log, label = generate_log(anomaly)
        logs.append(log)
        labels.append(label)

    df = pd.DataFrame({"log": logs, "label": labels})
    df.to_csv("data/synthetic_logs.csv", index=False)
    print("Dataset saved -> data/synthetic_logs.csv")

if __name__ == "__main__":
    create_dataset()