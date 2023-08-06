import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='darkgrid')


def plot_neuron(neuron):
    """render plot for neuron"""
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.lineplot(x=neuron.t, y=neuron.v)
    ax.set_title('voltage for ' + neuron.name)
    ax.set_ylabel('voltage (mV)')
    ax.set_xlabel('time (ms)')

    plt.show()


def plot_neurons(output_neurons):
    for neuron in output_neurons.values():
        plot_neuron(neuron)
