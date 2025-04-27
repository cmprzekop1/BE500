#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🔵 Installing Python requirements..."
pip install -r requirements.txt

echo "🔵 Running cohort simulation for multiple patients..."

# Customize how many patients you want to simulate:
NUM_PATIENTS=20

for (( patient_id=1; patient_id<=NUM_PATIENTS; patient_id++ ))
do
    echo "  ➔ Simulating patient $patient_id..."
    python cohort_simulation.py --patient_id $patient_id
done

echo "🔵 Analyzing results..."
python analyze_results.py

echo "🔵 Starting dashboard..."
python dashboard.py

echo "✅ All steps completed successfully!"
