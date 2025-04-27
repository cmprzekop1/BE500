class PIDController:
    def __init__(self, target_glucose=110, Kp=0.1, Ki=0.01, Kd=0.05, u_max=10.0, integral_limit=1000.0):
        self.target_glucose = target_glucose
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.u_max = u_max
        self.integral_error = 0.0
        self.prev_error = 0.0
        self.integral_limit = integral_limit  # <-- Anti-windup clamp limit

    def compute(self, time, states, parameters, dt=1.0):
        G, X, I = states
        error = self.target_glucose - G
        # Only clip very low glucose (hypoglycemia protection)
        if G < 70:  # Only if true hypo, shut off insulin
            error = 0
        # Update integral
        self.integral_error += error * dt
        self.integral_error = max(-self.integral_limit, min(self.integral_error, self.integral_limit))

        # Derivative term
        derivative_error = (error - self.prev_error) / dt
        self.prev_error = error

        # PID formula
        u = (self.Kp * error) + (self.Ki * self.integral_error) + (self.Kd * derivative_error)

        # Clip output
        u = max(0.0, min(u, self.u_max))

        return u
