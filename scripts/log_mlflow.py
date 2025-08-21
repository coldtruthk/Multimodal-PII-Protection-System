import os
import time
import random

from dotenv import load_dotenv
import mlflow

load_dotenv()
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns"))
mlflow.set_experiment("pii-dev")

with mlflow.start_run(run_name="hello-mlflow") as run:
    mlflow.log_param("model", "ner-koelectra")
    mlflow.log_param("lr", 5e-5)
    # 가짜 지표
    f1 = 0.80 + random.random() * 0.05
    loss = 0.5 - random.random() * 0.1
    time.sleep(0.5)
    mlflow.log_metric("f1", f1)
    mlflow.log_metric("loss", loss)
    print("run_id:", run.info.run_id)
