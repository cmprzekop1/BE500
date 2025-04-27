import numpy as np
import pandas as pd
import os

def compute_metrics(times, states):
    glucose = states[:, 0]
    tir = np.mean((glucose >= 70) & (glucose <= 180)) * 100
    avg_glucose = np.mean(glucose)
    cv_glucose = np.std(glucose) / avg_glucose * 100
    return {"TIR (%)": tir, "Avg Glucose (mg/dL)": avg_glucose, "CV (%)": cv_glucose}

def save_metrics_csv(metrics_dict, Kp_label, patient_folder):
    df = pd.DataFrame([metrics_dict])
    df.to_csv(os.path.join(patient_folder, f"metrics_{Kp_label}.csv"), index=False)
