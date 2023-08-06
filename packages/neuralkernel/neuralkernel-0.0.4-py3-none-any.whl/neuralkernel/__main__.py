from .graph import plot_neurons
from .spikekernel import simulate_neurons


def main():
    output_neurons = simulate_neurons('maximum', {'input': [200, 240],
                                                  'inputtwo': [200, 290]})
    # output_neurons = simulate_neurons('inverting_mem',
    #                                   {'input': [200, 290], 'recall': [500]})
    # output_neurons = simulate_neurons('non_inverting_mem', {
    #     'input': [200, 220], 'recall': [500]})
    # output_neurons = simulate_neurons('full_subtractor',
    #                                   {'inputone': [200, 290],
    #                                    'inputtwo': [200, 240]
    #                                    })
    # output_neurons = simulate_neurons('logarithm',
    #                                   {'input': [200, 270]})
    plot_neurons(output_neurons)


if __name__ == '__main__':
    main()
