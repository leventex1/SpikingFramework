from spyke.neuron import Neuron, SpikingNeuron, Synapse

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

before_membrane_change = False
def test_membrane_change_f(neuron: Neuron, time_step: int) -> None:
    global before_membrane_change
    before_membrane_change = True
    assert time_step == 1
    assert neuron.id == 7

n3 = SpikingNeuron(0, 0, 1, None, test_membrane_change_f)
n3.on_before_membrane_change(1)
assert before_membrane_change