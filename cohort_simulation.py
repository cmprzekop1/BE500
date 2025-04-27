import os
import argparse
import numpy as np
from simulate_patient import simulate_patient
from plotting.plotting import plot_patient
from metrics.metrics import save_metrics_csv
from cohort_compare import cohort_compare_openloop_vs_pid

def main():
    # Argument parser
    parser = argparse.ArgumentParser(description="Simulate a single patient with multiple PID gains.")
    parser.add_argument('--patient_id', type=int, required=True, help="ID number for the patient (integer)")
    args = parser.parse_args()
    patient_id = args.patient_id

    # Settings
    pid_gains = [0.0, 0.01, 0.05, 0.1, 0.2]  # Include OpenLoop (Kp=0.0)
    results_base = "results"
    os.makedirs(results_base, exist_ok=True)

    # Random patient parameters
    params = {
        "p1": 0.02,
        "p2": 0.025,
        "p3": 0.00013,
        "n": 0.05,
        "gamma": 0.005,
        "h": 110,
        "Gb": 110,
        "Ib": np.random.uniform(10, 20)
    }

    # Random basal rate
    basal_rate = np.random.uniform(0.7, 0.9)

    print(f"\n=== Simulating Patient {patient_id} ===")
    print(f"Randomized Ib = {params['Ib']:.2f}, Basal rate = {basal_rate:.2f} U/hr")

    # Simulate
    results = simulate_patient(patient_id, params, pid_gains, seed=42, basal_rate=basal_rate)

    # Save to folder
    patient_folder = os.path.join(results_base, f"patient_{patient_id:03d}")
    os.makedirs(patient_folder, exist_ok=True)

    for Kp_label, data in results.items():
        plot_patient(data['times'], data['states'], Kp_label, patient_folder)
        plot_patient_detailed(data['times'], data['states'], Kp_label, patient_folder)
        save_metrics_csv(data['metrics'], Kp_label, patient_folder)

    print(f"Patient {patient_id} complete. Results saved to {patient_folder}\n")
    cohort_compare_openloop_vs_pid(results_base="results", kp_values=[0.0, 0.01, 0.05, 0.1, 0.2], output_folder="results")
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_patient_detailed(times, states, Kp_label, output_folder):
    glucose = states[:, 0]
    insulin = states[:, 2]
    insulin_action = states[:, 1]

    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    axs[0].plot(times, glucose)
    axs[0].set_ylabel("Glucose (mg/dL)")
    axs[0].set_title(f"Glucose ({Kp_label})")
    axs[0].grid(True)

    axs[1].plot(times, insulin)
    axs[1].set_ylabel("Insulin (U/mL)")
    axs[1].set_title("Plasma Insulin")
    axs[1].grid(True)

    axs[2].plot(times, insulin_action)
    axs[2].set_ylabel("Insulin Action (X)")
    axs[2].set_xlabel("Time (minutes)")
    axs[2].set_title("Insulin Action")
    axs[2].grid(True)

    plt.tight_layout()

    save_path = os.path.join(output_folder, f"detailed_plot_{Kp_label}.png")
    plt.savefig(save_path)
    plt.close()

if __name__ == "__main__":
    main()