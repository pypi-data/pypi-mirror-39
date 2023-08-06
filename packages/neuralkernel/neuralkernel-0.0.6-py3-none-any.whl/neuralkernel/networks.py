from collections import namedtuple

from .constants import W_E, W_ACC, W_BAR_ACC, W_I, G_MULT, T_SYN, T_MIN, T_NEU
from .synapse import Synapse, SynapseGroupKey

Network = namedtuple("Network",
                     ("window", "output_neuron_names", "neuron_names",
                      "synapses"))

logarithm = Network(500, {"output"},
                    ["input", "first", "last", "acc", "output"],
                    {
                        SynapseGroupKey("input", "first"): [
                            Synapse("v", W_E, T_SYN)
                        ],
                        SynapseGroupKey("first", "first"): [
                            Synapse("v", W_I, T_SYN)
                        ],
                        SynapseGroupKey("input", "last"): [
                            Synapse("v", 0.5 * W_E, T_SYN)
                        ],
                        SynapseGroupKey("first", "acc"): [
                            Synapse("ge", W_BAR_ACC, T_SYN + T_MIN)
                        ],
                        SynapseGroupKey("last", "acc"): [
                            Synapse("ge", -W_BAR_ACC, T_SYN),
                            Synapse("gf", G_MULT, T_SYN),
                            Synapse("gate", 1, T_SYN)
                        ],
                        SynapseGroupKey("last", "output"): [
                            Synapse("v", W_E, 2 * T_SYN)
                        ],
                        SynapseGroupKey("acc", "output"): [
                            Synapse("v", W_E, T_SYN + T_MIN)
                        ]
                    })

maximum = Network(1000, {"output"},
                  ["input", "inputtwo", "larger", "largertwo", "output"],
                  {
                      SynapseGroupKey("input", "largertwo"): [
                          Synapse("v", 0.5 * W_E, T_SYN)
                      ],
                      SynapseGroupKey("input", "output"): [
                          Synapse("v", 0.5 * W_E, T_SYN)
                      ],
                      SynapseGroupKey("inputtwo", "output"): [
                          Synapse("v", 0.5 * W_E, T_SYN)
                      ],
                      SynapseGroupKey("inputtwo", "larger"): [
                          Synapse("v", 0.5 * W_E, T_SYN + T_MIN)
                      ],
                      SynapseGroupKey("larger", "largertwo"): [
                          Synapse("v", W_I, T_SYN),
                      ],
                      SynapseGroupKey("largertwo", "larger"): [
                          Synapse("v", W_I, T_SYN)
                      ]
                  })

inverting_mem = Network(800, {"output"},
                        ["input", "first", "last", "acc", "recall", "output"],
                        {
                            SynapseGroupKey("input", "first"): [
                                Synapse("v", W_E, T_SYN)
                            ],
                            SynapseGroupKey("first", "first"): [
                                Synapse("v", W_I, T_SYN)
                            ],
                            SynapseGroupKey("input", "last"): [
                                Synapse("v", 0.5 * W_E, T_SYN)
                            ],
                            SynapseGroupKey("first", "acc"): [
                                Synapse("ge", W_ACC, T_SYN + T_MIN)
                            ],
                            SynapseGroupKey("last", "acc"): [
                                Synapse("ge", -W_ACC, T_SYN),
                            ],
                            SynapseGroupKey("acc", "output"): [
                                Synapse("v", W_E, T_SYN)
                            ],
                            SynapseGroupKey("recall", "acc"): [
                                Synapse("ge", W_ACC, T_SYN)
                            ],
                            SynapseGroupKey("recall", "output"): [
                                Synapse("v", W_E, 2 * T_SYN)
                            ]
                        })

non_inverting_mem = Network(800, {"output"},
                            ["input", "first", "last", "acc", "acctwo",
                             "recall", "ready", "output"],
                            {
                                SynapseGroupKey("input", "first"): [
                                    Synapse("v", W_E, T_SYN)
                                ],
                                SynapseGroupKey("first", "first"): [
                                    Synapse("v", W_I, T_SYN)
                                ],
                                SynapseGroupKey("input", "last"): [
                                    Synapse("v", 0.5 * W_E, T_SYN)
                                ],
                                SynapseGroupKey("first", "acc"): [
                                    Synapse("ge", W_ACC, T_SYN)
                                ],
                                SynapseGroupKey("acc", "acctwo"): [
                                    Synapse("ge", -W_ACC, T_SYN)
                                ],
                                SynapseGroupKey("last", "acctwo"): [
                                    Synapse("ge", W_ACC, T_SYN)
                                ],
                                SynapseGroupKey("acc", "ready"): [
                                    Synapse("v", W_E, T_SYN)
                                ],
                                SynapseGroupKey("recall", "acctwo"): [
                                    Synapse("ge", W_ACC, T_SYN)
                                ],
                                SynapseGroupKey("recall", "output"): [
                                    Synapse("v", W_E, T_SYN)
                                ],
                                SynapseGroupKey("acctwo", "output"): [
                                    Synapse("v", W_E, T_SYN)
                                ]
                            })

full_subtractor = Network(1000, {"output+", "output-"},
                          ["inputone", "inputtwo", "syncone",
                           "synctwo", "inbone", "inbtwo", "output+",
                           "output-", "zero"],
                          {
                              SynapseGroupKey("inputone", "syncone"): [
                                  Synapse("v", 0.5 * W_E, T_SYN)
                              ],
                              SynapseGroupKey("inputtwo", "synctwo"): [
                                  Synapse("v", 0.5 * W_E, T_SYN)
                              ],
                              SynapseGroupKey("syncone", "output+"): [
                                  Synapse("v", W_E,
                                          T_MIN + 3 * T_SYN + 2 * T_NEU)
                              ],
                              SynapseGroupKey("syncone", "inbone"): [
                                  Synapse("v", W_E, T_SYN)
                              ],
                              SynapseGroupKey("syncone", "output-"): [
                                  Synapse("v", W_E, 3 * T_SYN + 2 * T_NEU)
                              ],
                              SynapseGroupKey("syncone", "inbtwo"): [
                                  Synapse("v", W_I, T_SYN)
                              ],
                              SynapseGroupKey("synctwo", "inbone"): [
                                  Synapse("v", W_I, T_SYN)
                              ],
                              SynapseGroupKey("synctwo", "output+"): [
                                  Synapse("v", W_E, 3 * T_SYN + 2 * T_NEU)
                              ],
                              SynapseGroupKey("synctwo", "inbtwo"): [
                                  Synapse("v", W_E, T_SYN)
                              ],
                              SynapseGroupKey("synctwo", "output-"): [
                                  Synapse("v", W_E,
                                          T_MIN + 3 * T_SYN + 2 * T_NEU)
                              ],
                              SynapseGroupKey("inbone", "output+"): [
                                  Synapse("v", 2 * W_I, T_SYN)
                              ],
                              SynapseGroupKey("inbtwo", "output-"): [
                                  Synapse("v", 2 * W_I, T_SYN)
                              ],
                              SynapseGroupKey("output+", "inbtwo"): [
                                  Synapse("v", 0.5 * W_E, T_SYN)
                              ],
                              SynapseGroupKey("output-", "inbone"): [
                                  Synapse("v", 0.5 * W_E, T_SYN)
                              ],
                              SynapseGroupKey("zero", "zero"): [
                                  Synapse("v", W_E, T_NEU)
                              ],
                              SynapseGroupKey("synctwo", "zero"): [
                                  Synapse("v", 0.5 * W_E, T_NEU),
                                  Synapse("v", 0.5 * W_I, 2 * T_NEU)
                              ],
                              SynapseGroupKey("syncone", "zero"): [
                                  Synapse("v", 0.5 * W_E, T_NEU),
                                  Synapse("v", 0.5 * W_I, 2 * T_NEU)
                              ],
                              SynapseGroupKey("zero", "inbtwo"): [
                                  Synapse("v", W_I, T_NEU),
                              ],
                              SynapseGroupKey("zero", "output-"): [
                                  Synapse("v", 2 * W_I, T_NEU),
                              ]
                          })

available_networks = {
    "logarithm": logarithm,
    "maximum": maximum,
    "inverting_mem": inverting_mem,
    "non_inverting_mem": non_inverting_mem,
    "full_subtractor": full_subtractor
}
