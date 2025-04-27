import numpy as np
import matplotlib.pyplot as plt
import os

def cohort_compare_openloop_vs_pid(results_base, kp_values, output_folder):
    kp_means = {kp: [] for kp in kp_values}

    patient_folders = sorted([f for f in os.listdir(results_base) if f.startswith("patient_")])

    for patient_folder in patient_folders:
        patient_path = os.path.join(results_base, patient_folder)
        for kp in kp_values:
            kp_label = f"Kp_{kp:.3f}"
            file_path = os.path.join(patient_path, f"metrics_{kp_label}.csv")
            glucose_file = os.path.join(patient_path, f"glucose_Kp_{kp:.3f}.npy")  # Assuming you saved glucose as .npy too
            if os.path.exists(glucose_file):
                glucose_traj = np.load(glucose_file)
                kp_means[kp].append(glucose_traj)

    plt.figure(figsize=(10, 6))

    # Plot Open Loop (Kp=0.000)
    if 0.0 in kp_means and kp_means[0.0]:
        glucose_open_mean = np.mean(kp_means[0.0], axis=0)
        times = np.arange(len(glucose_open_mean))
        plt.plot(times, glucose_open_mean, label="Open Loop (No PID)", color='red', linestyle='--', linewidth=2)

    # Plot PID (Kp > 0)
    for kp in kp_values:
        if kp == 0.0:
            continue
        if kp_means[kp]:
            glucose_pid_mean = np.mean(kp_means[kp], axis=0)
            times = np.arange(len(glucose_pid_mean))
            plt.plot(times, glucose_pid_mean, label=f"PID (Kp={kp:.3f})", alpha=0.8)

    # Threshold lines
    plt.axhline(70, color='blue', linestyle=':', label='Hypoglycemia Threshold (70)')
    plt.axhline(180, color='orange', linestyle=':', label='Hyperglycemia Threshold (180)')
    plt.axhline(110, color='green', linestyle='-.', label='Target Glucose (110)')

    plt.xlabel("Time (minutes)")
    plt.ylabel("Glucose (mg/dL)")
    plt.title("Cohort Comparison: Open Loop vs PID Control (Mean Glucose)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    save_path = os.path.join(output_folder, "cohort_compare_openloop_vs_pid.png")
    plt.savefig(save_path)
    plt.close()

    print(f"Saved cohort comparison plot to {save_path}")
