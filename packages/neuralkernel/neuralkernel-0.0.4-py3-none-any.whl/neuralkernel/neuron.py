import numpy as np

from .constants import V_THRESHOLD, TAU_F, TAU_M


class Neuron:
    OFFSET_TO_GATE_WEIGHT = {1: 1, -1: 0}

    def __init__(self, name, t):
        self.name = name
        self.t = t
        self.v = np.zeros(t.shape)
        self.ge = np.zeros(t.shape)
        self.gf = np.zeros(t.shape)
        self.gate = np.zeros(t.shape)

    def set_spikes(self, spike_times):
        self.v[np.array(spike_times)] = V_THRESHOLD

    def is_spike(self, time):
        return self.v[time] >= V_THRESHOLD

    def update(self, field, idx, offset):
        """general update of neuron state variable"""

        if field in {"v", "ge", "gf"}:
            getattr(self, field)[idx] += offset
        elif field == "gate":
            getattr(self, field)[idx] = self.OFFSET_TO_GATE_WEIGHT[offset]
        else:
            raise ValueError("field " + str(field) + " not supported")

    def simulate(self, idx):
        """simulate neuron at index"""

        if self.v[idx - 1] >= V_THRESHOLD:
            v_prev = 0
            ge_prev = 0
            gf_prev = 0
            gate_prev = 0
        else:
            v_prev = self.v[idx - 1]
            ge_prev = self.ge[idx - 1]
            gf_prev = self.gf[idx - 1]
            gate_prev = self.gate[idx - 1]
        dt = self.t[idx] - self.t[idx - 1]
        self.ge[idx] += ge_prev
        self.gate[idx] = max([self.gate[idx], gate_prev])
        self.gf[idx] += gf_prev + dt * (-gf_prev / TAU_F)
        self.v[idx] += v_prev + dt * ((ge_prev + gf_prev * gate_prev) / TAU_M)
