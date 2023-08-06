import numpy as np

from .networks import available_networks
from .neuron import Neuron
from .synapse import SynapseMatrix


def simulate_neurons(network_name, offsets):
    """simulate neuron network with given voltage offsets"""

    # simulation parameters
    network = available_networks[network_name]
    t = np.arange(network.window)
    neurons = {neuron_name: Neuron(neuron_name, t) for neuron_name in
               network.neuron_names}

    # set spikes
    for neuron_name in offsets:
        neurons[neuron_name].set_spikes(offsets[neuron_name])

    # run synapse matrix
    adj_matrix = SynapseMatrix(neurons, network.synapses)
    adj_matrix.simulate(t)

    # fill in output neurons
    output_neurons = {}
    for neuron in adj_matrix.neurons:
        if neuron in network.output_neuron_names:
            # copy neuron reference
            output_neurons[neuron] = adj_matrix.neurons[neuron]

    return output_neurons
