from neuron import Neuron, SpikingNeuron, Synapse

assert SpikingNeuron().id == 0 and SpikingNeuron().id == 1

assert SpikingNeuron(0.0, 0.0, 1.0).is_fireing() == False
assert SpikingNeuron(0.0, 1.0, 1.0).is_fireing() == True
assert SpikingNeuron(0.0, 2.0, 1.0).is_fireing() == True

n1 = SpikingNeuron(0.0, 1.0, 1.0)
n1.reset_neuron()
assert n1.get_membrane_value() == 0.0

n2 = SpikingNeuron()
n1.add_connection(Synapse(1.0, n2))
assert len(n2.connections) == 0

t = 0
def test_f(neruon: Neuron) -> None:
    global t
    t = 1
n1.on_fireing_callback = test_f
n1.on_fireing()
assert t == 1