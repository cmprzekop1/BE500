def open_loop_controller(time, states, parameters):
    """
    Open loop: no feedback control, just constant basal input.
    """
    u = 0.0  # No additional insulin
    return u
class OpenLoopController:
    def compute(self, t, states, parameters, dt=1.0):
        """
        Open loop controller: Always returns 0 bolus.
        """
        return 0.0
