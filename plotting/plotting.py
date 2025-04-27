import os
import matplotlib.pyplot as plt

def plot_patient(times, states, Kp_label, patient_folder):
    glucose = states[:, 0]
    insulin_action = states[:, 1]
    insulin_concentration = states[:, 2]

    # Special label if open loop (Kp = 0)
    if Kp_label.startswith("Kp_0.000"):
        title = "Open Loop (No PID)"
        filename = "plot_OpenLoop.png"
    else:
        title = f"PID Control ({Kp_label})"
        filename = f"plot_{Kp_label}.png"

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(times, glucose, label="Blood Glucose (mg/dL)")
    plt.axhline(70, color="red", linestyle="--", label="Hypoglycemia Threshold (70)")
    plt.axhline(180, color="orange", linestyle="--", label="Hyperglycemia Threshold (180)")
    plt.title(title)
    plt.xlabel("Time (minutes)")
    plt.ylabel("Glucose (mg/dL)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    save_path = os.path.join(patient_folder, filename)
    plt.savefig(save_path)
    plt.close()
