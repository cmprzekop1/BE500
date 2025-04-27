import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Paths
results_base = "results"
output_summary_csv = os.path.join(results_base, "cohort_summary.csv")
output_plot_dir = os.path.join(results_base, "plots")
os.makedirs(output_plot_dir, exist_ok=True)

# Gather patient folders
patient_folders = sorted([f for f in os.listdir(results_base) if f.startswith("patient_")])

# Initialize empty dataframe list
full_results = []

# Gather data
for patient_folder in patient_folders:
    patient_path = os.path.join(results_base, patient_folder)  # <-- ADD THIS LINE BEFORE USING patient_path
    for file in os.listdir(patient_path):
        if file.startswith("metrics_Kp_") and file.endswith(".csv"):
            # Robust float parsing to handle trailing zeros
            kp_str = file.split("_")[2].replace(".csv", "")
            kp_value = round(float(kp_str), 3)
            metrics_df = pd.read_csv(os.path.join(patient_path, file))
            metrics_df["PatientID"] = int(patient_folder.split("_")[1])
            metrics_df["Kp"] = kp_value
            full_results.append(metrics_df)

# Combine all into one table
if full_results:
    df = pd.concat(full_results, ignore_index=True)
    df.to_csv(output_summary_csv, index=False)
    print(f"Cohort summary saved to {output_summary_csv}")
else:
    print("No results found! Exiting.")
    exit()

# --------------------------------
# 🎨 Seaborn Plots
# --------------------------------

sns.set(style="whitegrid", font_scale=1.4)

# TIR Comparison
plt.figure(figsize=(8, 6))
sns.boxplot(x="Kp", y="TIR (%)", data=df, palette="Set2")
sns.swarmplot(x="Kp", y="TIR (%)", data=df, color=".25", size=4)
plt.title("Time in Range (%) vs PID Kp")
plt.xlabel("Kp Value")
plt.ylabel("Time in Range (%)")
plt.tight_layout()
plt.savefig(os.path.join(output_plot_dir, "tir_vs_kp.png"))
plt.close()

# Average Glucose
plt.figure(figsize=(8, 6))
sns.boxplot(x="Kp", y="Avg Glucose (mg/dL)", data=df, palette="Set2")
sns.swarmplot(x="Kp", y="Avg Glucose (mg/dL)", data=df, color=".25", size=4)
plt.title("Average Glucose vs PID Kp")
plt.xlabel("Kp Value")
plt.ylabel("Average Glucose (mg/dL)")
plt.tight_layout()
plt.savefig(os.path.join(output_plot_dir, "avg_glucose_vs_kp.png"))
plt.close()

# Glucose CV%
plt.figure(figsize=(8, 6))
sns.boxplot(x="Kp", y="CV (%)", data=df, palette="Set2")
sns.swarmplot(x="Kp", y="CV (%)", data=df, color=".25", size=4)
plt.title("Coefficient of Variation (%) vs PID Kp")
plt.xlabel("Kp Value")
plt.ylabel("Glucose CV (%)")
plt.tight_layout()
plt.savefig(os.path.join(output_plot_dir, "cv_vs_kp.png"))
plt.close()

print(f"All cohort boxplots saved to {output_plot_dir}")
