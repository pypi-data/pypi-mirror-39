import matplotlib.pyplot as plt
import numpy as np


def plot_neurons(output_neurons):
    fig = plt.figure(1, figsize=(15, 10), facecolor='white')
    big_ax = fig.add_subplot(111)  # overarching subplot

    # turn off axis lines and ticks of the big subplot
    big_ax.spines['top'].set_color('none')
    big_ax.spines['bottom'].set_color('none')
    big_ax.spines['left'].set_color('none')
    big_ax.spines['right'].set_color('none')
    big_ax.tick_params(labelcolor='w', top='off', bottom='off', left='off',
                       right='off')
    big_ax.set_xlabel('time (ms)')
    big_ax.set_ylabel('voltage (mV)')

    # plot
    i = 0
    for neuron_name, neuron in output_neurons.items():
        subplot_num = int(str(len(output_neurons)) + "1" + str(i + 1))
        ax = fig.add_subplot(subplot_num)
        ax.plot(neuron.t, neuron.v)
        ax.set_title('voltage for ' + neuron.name)
        start, end = ax.get_xlim()
        ax.xaxis.set_ticks(np.arange(start, end, 100))
        ax.grid(True)
        i += 1

    plt.show()
