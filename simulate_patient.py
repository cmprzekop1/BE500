import numpy as np
from solvers.ode_solvers import rk4_step
from models.glucose_insulin_model import glucose_insulin_ode
from controllers.open_loop import OpenLoopController
from controllers.pid_controller import PIDController
from metrics.metrics import compute_metrics

def simulate_patient(patient_id, params, pid_gains, seed=42, basal_rate=0.8):
    np.random.seed(seed + patient_id)
    parameters = np.array(list(params.values()))

    T_end = 1440  # 24 hours
    dt = 1  # minutes
    times = np.arange(0, T_end, dt)

    # Initial state: [glucose, insulin action, plasma insulin]
    initial_states = np.array([np.random.uniform(110, 130), 0.0, params['Ib']])

    # Meal schedule
    meal_times = np.array([300, 600, 1000])  # minutes
    meal_sizes = np.random.uniform(80, 120, size=len(meal_times))  # grams

    # Basal insulin drift (for PID only)
    basal_rate_variation = np.random.normal(0.0, 0.1, size=len(times))

    results = {}

    for Kp in pid_gains:
        if Kp == 0.0:
            controller_type = "OpenLoop"
            controller = OpenLoopController()
        else:
            controller_type = f"PID (Kp={Kp:.3f})"
            Ki = 0.3 * Kp
            Kd = 0.5 * Kp
            controller = PIDController(target_glucose=110, Kp=Kp, Ki=Ki, Kd=Kd, u_max=0.2)

        states = initial_states.copy()
        history = np.zeros((len(times), len(states)))

        for idx, t in enumerate(times):
            # Meal absorption
            meal_effect = sum(
                (size / 120.0) * 0.3
                for meal_time, size in zip(meal_times, meal_sizes)
                if meal_time <= t < meal_time + 120
            )

            # Hypoglycemia rescue
            rescue_carb = 0
            if states[0] < 70:
                rescue_carb = 15 / 120.0

            # Apply exogenous glucose effects
            states[0] += (meal_effect + rescue_carb) * dt

            # Basal insulin
            if Kp == 0.0:
                basal_u = 0.0
            else:
                drifted_basal = basal_rate * (1.0 + basal_rate_variation[idx])
                basal_u = drifted_basal / 60.0

            # Bolus insulin
            if Kp == 0.0:
                if t in meal_times:
                    idx_meal = np.where(meal_times == t)[0][0]
                    meal_size = meal_sizes[idx_meal]
                    bolus_u = meal_size / 10.0  # Simple carb counting (1 unit per 10g carbs)
                else:
                    bolus_u = 0.0
            else:
                bolus_u = controller.compute(t, states, parameters, dt=dt)

            # Total insulin input
            total_insulin = basal_u + bolus_u

            # Advance simulation
            states = rk4_step(glucose_insulin_ode, dt, states, t, parameters, total_insulin)

            # Clip physiological ranges
            states[0] = np.clip(states[0], 40, 600)
            states[1] = np.clip(states[1], 0, 500)
            states[2] = np.clip(states[2], 0, 1000)

            # Save history
            history[idx] = states

        results[f"Kp_{Kp:.3f}"] = {
            "times": times,
            "states": history,
            "metrics": compute_metrics(times, history),
            "controller": controller_type
        }

    return results