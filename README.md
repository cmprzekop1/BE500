
## Overview

This project simulates virtual patients' glucose-insulin dynamics across a 24-hour day, using either:
- **Open-loop control** (manual mealtime boluses)
- or **PID feedback control** (automated insulin dosing).

Each simulation generates:
- Glucose, plasma insulin, and insulin action time series
- Metrics (average glucose, time-in-range, coefficient of variation)
- Plots showing glucose trajectories and insulin delivery patterns

---

## Project Structure

```
FinalProjCode/
├── cohort_simulation.py        # Run simulation for a single patient
├── simulate_patient.py         # Core simulation logic
├── models/
│   └── glucose_insulin_model.py  # Glucose-insulin differential equations
├── solvers/
│   └── ode_solvers.py            # 4th-order Runge-Kutta (RK4) integration
├── controllers/
│   ├── open_loop.py              # Open-loop (fixed bolus) controller
│   └── pid_controller.py         # PID controller (feedback insulin control)
├── metrics/
│   └── metrics.py                # Metric computation (TIR, CV%, Avg Glucose)
├── plotting/
│   └── plotting.py               # Plot generation
├── results/                     # Simulation outputs (plots, CSVs)
│   └── patient_001/              # Example patient results
├── cohort_compare.py             # Compare cohort performance across Kp values
└── README.md                     # (this file)
```

---

## How to Run

First, install required Python packages:

```bash
pip install -r requirements.txt
```

Then, to simulate a patient:

```bash
python cohort_simulation.py --patient_id 1
```

This will:
- Randomize patient parameters (insulin sensitivity, basal needs)
- Run OpenLoop and PID controller simulations
- Save results into `results/patient_001/`
- Generate summary plots and cohort comparison charts

---

## Output Files

For each patient, saved under `results/patient_XXX/`:
- `metrics_PID_Kp_0.010.csv` : Metrics for each Kp value
- `plot_PID_Kp_0.010.png` : Glucose, Insulin, Insulin Action plots
- `plot_OpenLoop.png` : Open-loop baseline plots

Across all patients:
- `cohort_summary.csv` : All simulation metrics compiled
- `plots/` : Boxplots comparing TIR, Avg Glucose, CV% vs Kp

---

## 🎯 Controller Behavior

| Controller | Behavior |
|:---|:---|
| OpenLoop | Manual mealtime boluses (fixed, no feedback) |
| PID Controller | Dynamic insulin delivery to regulate glucose at 110 mg/dL |

When using PID, there are **no manual meal boluses** — the controller fully handles glucose spikes.

---

## Cohort Analysis

After simulating multiple patients, you can generate:
- Boxplots: Time-in-Range (TIR) vs Kp
- Boxplots: Average Glucose vs Kp
- Boxplots: Coefficient of Variation (CV%) vs Kp

These plots are saved automatically into `results/plots/`.


#Quick Start

```bash
pip install -r requirements.txt
python cohort_simulation.py --patient_id 1
```

or chmod +x run_pipeline.sh
then ./run_pipeline.sh
