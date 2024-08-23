from random import random
from spyke.neuron import Synapse, SpikingNeuron
from spyke.spikingengine import SpikingEngine, QueueProcessNeuronFire, QueueProcessNeuronSend
from spyke.dynamics import Counter, SynapticUpdater

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

    n1.add_connection(Synapse(0.3, n4))
    n2.add_connection(Synapse(0.3, n4))
    n3.add_connection(Synapse(0.1, n4))

    while counter.get_current_time_step() < 50000:
        n1.change_membrane_value((random() < 0.2) * 1.0)
        n2.change_membrane_value((random() < 0.2) * 1.0)
        n3.change_membrane_value((random() < 0.5) * 1.0)
        engine.add_process(QueueProcessNeuronFire(n1, engine))
        engine.add_process(QueueProcessNeuronFire(n2, engine))
        engine.add_process(QueueProcessNeuronFire(n3, engine))

        engine.process_cycle()

        print(f'counter({counter.get_current_time_step()})', end=': ')
        for back_ref in n4.back_refs:
            synapse: Synapse = back_ref.connection
            print("{:.2f}".format(synapse.weight), end=', ')
        print()
