from random import random
import numpy as np
import matplotlib.pyplot as plt
from spyke.neuron import Synapse, SpikingNeuron
from spyke.spikingengine import SpikingEngine, QueueProcessNeuronFire, QueueProcessNeuronSend
from spyke.dynamics import Counter, SynapticUpdater, exponent_membrane_decay

test_name = input('test name: ')

if test_name == 'simple spiking':
    def on_fireing(neuron: SpikingNeuron) -> None:
        print(f'neuron[{neuron.id}] fired.')

    graph = [
        SpikingNeuron(0.0, 1.0, 1.0, on_fireing),
        SpikingNeuron(0.0, 0.0, 1.0, on_fireing),
        SpikingNeuron(0.0, 0.0, 1.0, on_fireing),
        SpikingNeuron(0.0, 0.0, 1.0, on_fireing),
    ]

    graph[0].add_connection(Synapse(1.0, graph[1]))
    graph[0].add_connection(Synapse(1.0, graph[2]))
    graph[1].add_connection(Synapse(1.0, graph[2]))
    graph[2].add_connection(Synapse(1.0, graph[1]))

    counter = Counter(0.0, 0.5)
    engine = SpikingEngine(counter)

    engine.add_process(QueueProcessNeuronFire(graph[0], engine))

    while input('->') != 'q':
        print(f'counter: {counter.get_current_time_step()}')
        engine.process_cycle()

if test_name == 'test learning':
    synaptic_updater = SynapticUpdater()
    counter = Counter(0, 1)

    def on_fireing(neuron: SpikingNeuron) -> None:
        global counter
        global synaptic_updater
        t = counter.get_current_time_step()
        for connection in neuron.connections:
            synapse: Synapse = connection
            synapse.set_pre_fire_time_step(t)
            synaptic_updater.update_synapse(synapse)

        for back_connection in neuron.back_refs:
            synapse: Synapse = back_connection.connection
            synapse.set_post_fire_time_step(t)
            synaptic_updater.update_synapse(synapse)


    n1 = SpikingNeuron(0.0, 0.0, 1.0, on_fireing)
    n2 = SpikingNeuron(0.0, 0.0, 1.0, on_fireing)

    n1.add_connection(Synapse(0.5, n2))

    while counter.get_current_time_step() < 100:
        on_fireing(n1)
        counter.update()
        on_fireing(n2)

        print(counter.get_current_time_step(), n1.connections[0].weight)


if test_name == 'pattern learning':
    counter = Counter(0, 1)
    engine = SpikingEngine(counter)
    synaptic_updater = SynapticUpdater()

    def on_fireing(neuron: SpikingNeuron) -> None:
        global counter
        global synaptic_updater
        t = counter.get_current_time_step()
        for connection in neuron.connections:
            synapse: Synapse = connection
            synapse.set_pre_fire_time_step(t)
            synaptic_updater.update_synapse(synapse)

        for back_connection in neuron.back_refs:
            synapse: Synapse = back_connection.connection
            synapse.set_post_fire_time_step(t)
            synaptic_updater.update_synapse(synapse)


    n1 = SpikingNeuron(0.0, 0.0, 1.0, on_fireing)
    n2 = SpikingNeuron(0.0, 0.0, 1.0, on_fireing)
    n3 = SpikingNeuron(0.0, 0.0, 1.0, on_fireing)
    n4 = SpikingNeuron(0.0, 0.0, 1.0, on_fireing)

    n1.add_connection(Synapse(0.8, n4))
    n2.add_connection(Synapse(0.1, n4))
    n3.add_connection(Synapse(0.1, n4))

    while counter.get_current_time_step() < 50000:
        n1.change_membrane_value((random() < 0.19) * 1.0)
        n2.change_membrane_value((random() < 0.2) * 1.0)
        n3.change_membrane_value((random() < 0.21) * 1.0)
        engine.add_process(QueueProcessNeuronFire(n1, engine))
        engine.add_process(QueueProcessNeuronFire(n2, engine))
        engine.add_process(QueueProcessNeuronFire(n3, engine))

        engine.process_cycle()

        print(f'counter({counter.get_current_time_step()})', end=': ')
        for back_ref in n4.back_refs:
            synapse: Synapse = back_ref.connection
            print("{:.2f}".format(synapse.weight), end=', ')
        print()


if test_name == "mp test":
    np.random.seed(10)

    counter = Counter(0, 1)
    engine = SpikingEngine(counter)

    n1, n2, n3 = SpikingNeuron(), SpikingNeuron(), SpikingNeuron()

    n1.add_connection(Synapse(0.2, n2))
    n1.add_connection(Synapse(0.2, n3))
    n2.on_before_membrane_change_callback = lambda neuron, time_step: exponent_membrane_decay(neuron, time_step, 20)
    n3.on_before_membrane_change_callback = lambda neuron, time_step: exponent_membrane_decay(neuron, time_step, 20)

    potentials = []
    sampled_potentials = []
    while counter.get_current_time_step() < 100:
        if not n2.is_fireing():
            exponent_membrane_decay(n2, counter.get_current_time_step(), 20)

        n1.change_membrane_value((np.random.random() < 0.1) * 1.0)
        engine.add_process(QueueProcessNeuronFire(n1, engine))
        engine.process_cycle()

        potentials.append(n2.get_membrane_value())
        sampled_potentials.append(n3.get_membrane_value())
    
    times = [i for i in range(counter.get_current_time_step())]
    plt.plot(times, potentials, '-', times, sampled_potentials, 'r--')
    plt.ylabel('n2 member potentials')
    plt.xlabel('time steps')
    plt.show()


if test_name == 'logic test':
    """
    [0, 0] -> [0]
    [0, 1] -> [1]
    [1, 0] -> [1]
    [1, 1] -> [0]
    2 input node, both stimulied with a low rate < 0.05, but if there is an input bit the fireing rate is higher
    stimuli: 0 - ~20 time step, the stimuli time is separated into 2 section for the 2 input node
    [l...l.....l|...l......l.] -> [......l..l]  ([0, 0] -> [0])
    [l.........l|.l.ll.l.l.ll] -> [.l.ll.lll.]  ([0, 1] -> [1])
    [.l.ll.l.l.ll|l.........l] -> [.l.ll.lll.]  ([1, 0] -> [1])
    [.l..l.lll.ll|llll.ll..ll] -> [.l.....l..]  ([1, 1] -> [0])
    """
    examples: list[list[bool]] = [
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ]

    counter = Counter(0, 1)
    engine = SpikingEngine(counter)
    synaptic_updater = SynapticUpdater()

    def on_fireing_callback(neuron: SpikingNeuron) -> None:
        global counter
        global synaptic_updater
        t = counter.get_current_time_step()
        for connection in neuron.connections:
            synapse: Synapse = connection
            synapse.set_pre_fire_time_step(t)
            synaptic_updater.update_synapse(synapse)

        for back_connection in neuron.back_refs:
            synapse: Synapse = back_connection.connection
            synapse.set_post_fire_time_step(t)
            synaptic_updater.update_synapse(synapse)

    def before_membrane_change(neuron: SpikingNeuron, time_step: int) -> None:
        exponent_membrane_decay(neuron, time_step, 20)

    input_neuron_1 = SpikingNeuron(0, 0, 1, on_fireing_callback, before_membrane_change)
    input_neuron_2 = SpikingNeuron(0, 0, 1, on_fireing_callback, before_membrane_change)

    hidden_neuron_1 = SpikingNeuron(0, 0, 1, on_fireing_callback, before_membrane_change)
    hidden_neuron_2 = SpikingNeuron(0, 0, 1, on_fireing_callback, before_membrane_change)

    output_neuron = SpikingNeuron(0, 0, 1, on_fireing_callback, before_membrane_change)

    input_neuron_1.add_connection(Synapse(np.random.random(), hidden_neuron_1))
    input_neuron_1.add_connection(Synapse(np.random.random(), hidden_neuron_2))
    
    input_neuron_2.add_connection(Synapse(np.random.random(), hidden_neuron_1))
    input_neuron_2.add_connection(Synapse(np.random.random(), hidden_neuron_2))

    hidden_neuron_1.add_connection(Synapse(np.random.random(), output_neuron))
    hidden_neuron_2.add_connection(Synapse(np.random.random(), output_neuron))

    def get_inputs(input_1: bool, input_2: bool) -> list[int]:
        return [
            np.random.random() < (0.8 if input_1 else 0.05), 
            np.random.random() < (0.8 if input_2 else 0.05)
        ]

    episodes = 1000
    training_episodes = 980
    stimul_time = 20
    rest_time = 20
    
    episode = 0
    while episode < episodes:
        example = examples[np.random.randint(0, 4)]
        if episode > training_episodes:
            print(f'episode:{episode} ({example[0]},{example[1]}): {example[0] and example[1]}')        

        stimul_t = 0
        while stimul_t < stimul_time:
            stimul = get_inputs(example[0], example[1])

            input_neuron_1.change_membrane_value(stimul[0])
            input_neuron_2.change_membrane_value(stimul[1])
            engine.add_process(QueueProcessNeuronFire(input_neuron_1, engine))
            engine.add_process(QueueProcessNeuronFire(input_neuron_2, engine))
            engine.process_cycle()

            if episode <= training_episodes:
                if example[0] and example[1] and np.random.random() < 0.8:
                    on_fireing_callback(output_neuron)
            else:
                if output_neuron.is_fireing():
                    print('|', end='')
                else:
                    print('.', end='')

            stimul_t += 1

        rest_t = 0
        while rest_t < rest_time:
            engine.process_cycle()
            rest_t += 1

        print()
        episode += 1