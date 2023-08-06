from collections import namedtuple

from .constants import T_NEU

Synapse = namedtuple("Synapse", ("type", "weight", "delay"))
SynapseGroupKey = namedtuple("SynapseGroupKey", ("src", "dest"))


class SynapseMatrix:

    def __init__(self, neurons, synapses):
        self.neurons = neurons
        self.synapses = synapses

    def simulate(self, window):
        """simulate neurons in the adjacency matrix"""

        for time in window:
            for src in self.neurons.values():
                src.simulate(time)
                if src.is_spike(time):
                    # propagate across all destination neurons
                    for dest in self.neurons.values():
                        self.propagate_synapse(src, dest, time)

    def propagate_synapse(self, src, dest, synapse_time):
        """propagate synapse from src neuron to dest neuron"""

        synapse_key = SynapseGroupKey(src.name, dest.name)
        if synapse_key in self.synapses:
            for synapse in self.synapses[synapse_key]:
                # propagate
                synapse_time += synapse.delay + T_NEU
                self.neurons[dest.name].update(synapse.type, synapse_time,
                                               synapse.weight)
