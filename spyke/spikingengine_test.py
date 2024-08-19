from spikingengine import SpikingEngine, QueueProcessNeuronFire, QueueProcessNeuronSend, QueueProcessCycleEnd
from neuron import SpikingNeuron, Synapse


w = 1.0
n1, n2, n3 = SpikingNeuron(), SpikingNeuron(), SpikingNeuron()
n1.add_connection(Synapse(w, n2))
n3.add_connection(Synapse(-w, n2))

spiking_engine = SpikingEngine()
assert spiking_engine.process_queue.qsize() == 0


spiking_engine.add_process(QueueProcessNeuronFire(n1, spiking_engine))
spiking_engine.process_cycle()
assert spiking_engine.process_queue.qsize() == 0


n1.reset_neuron()
n2.reset_neuron()
n1.change_membrane_value(1.0)
spiking_engine.add_process(QueueProcessNeuronFire(n1, spiking_engine))
spiking_engine.process_cycle()  # Fire, End -> Send
assert n1.get_membrane_value() == n1.reset_value
assert spiking_engine.process_queue.qsize() == 1
assert type(spiking_engine.process_queue.get()) == QueueProcessNeuronSend


n1.reset_neuron()
n2.reset_neuron()
n1.change_membrane_value(1.0)
spiking_engine.add_process(QueueProcessNeuronFire(n1, spiking_engine))
spiking_engine.process_cycle()  # Fire, End -> Send
spiking_engine.process_cycle()  # Send, End -> Fire
assert n1.get_membrane_value() == n1.reset_value
assert n2.get_membrane_value() == w
assert spiking_engine.process_queue.qsize() == 1
assert type(spiking_engine.process_queue.get()) == QueueProcessNeuronFire


n1.reset_neuron()
n2.reset_neuron()
n1.change_membrane_value(1.0)
spiking_engine.add_process(QueueProcessNeuronFire(n1, spiking_engine))
spiking_engine.process_cycle()  # Fire, End -> Send
spiking_engine.process_cycle()  # Send, End -> Fire
spiking_engine.process_cycle()  # Fire, End -> Send
assert n1.get_membrane_value() == n1.reset_value
assert n2.get_membrane_value() == n2.reset_value
assert spiking_engine.process_queue.qsize() == 1
assert type(spiking_engine.process_queue.get()) == QueueProcessNeuronSend


n1.reset_neuron()
n2.reset_neuron()
n1.change_membrane_value(1.0)
spiking_engine.add_process(QueueProcessNeuronFire(n1, spiking_engine))
assert len(list(spiking_engine.process_queue.queue)) == 1
spiking_engine.process_cycle()  # Fire, End -> Send
assert len(list(spiking_engine.process_queue.queue)) == 1
spiking_engine.process_cycle()  # Send, End -> Fire
assert len(list(spiking_engine.process_queue.queue)) == 1
spiking_engine.process_cycle()  # Fire, End -> Send
assert len(list(spiking_engine.process_queue.queue)) == 1
spiking_engine.process_cycle()  # Send, End -> _
assert n1.get_membrane_value() == n1.reset_value
assert n2.get_membrane_value() == n2.reset_value
assert spiking_engine.process_queue.qsize() == 0


n1.reset_neuron()
n2.reset_neuron()
n3.reset_neuron()
n1.change_membrane_value(1.0)
n3.change_membrane_value(1.0)
spiking_engine.add_process(QueueProcessNeuronFire(n1, spiking_engine))
spiking_engine.add_process(QueueProcessNeuronFire(n3, spiking_engine))
assert len(list(spiking_engine.process_queue.queue)) == 2
spiking_engine.process_cycle()  # Fire, Fire, End -> Send, Send
assert len(list(spiking_engine.process_queue.queue)) == 2
l = list(spiking_engine.process_queue.queue)
assert type(l[0]) == QueueProcessNeuronSend and type(l[1]) == QueueProcessNeuronSend
spiking_engine.process_cycle()  # Send, Send, End -> Fire
assert len(list(spiking_engine.process_queue.queue)) == 1
l = list(spiking_engine.process_queue.queue)
assert type(l[0]) == QueueProcessNeuronFire
assert n2.get_membrane_value() == 0.0
spiking_engine.process_cycle()  # Fire, End -> _
assert len(list(spiking_engine.process_queue.queue)) == 0
assert n1.get_membrane_value() == n1.reset_value
assert n3.get_membrane_value() == n3.reset_value


n1.add_connection(Synapse(w, n3))
n3.add_connection(Synapse(w, n1))
n1.reset_neuron()
n2.reset_neuron()
n3.reset_neuron()
n1.change_membrane_value(1.0)
n3.change_membrane_value(1.0)
spiking_engine.add_process(QueueProcessNeuronFire(n1, spiking_engine))
spiking_engine.add_process(QueueProcessNeuronFire(n3, spiking_engine))
spiking_engine.process_cycle()  # Fire, Fire, End -> Send, Send
l = list(spiking_engine.process_queue.queue)
assert type(l[0]) == QueueProcessNeuronSend and type(l[1]) == QueueProcessNeuronSend
spiking_engine.process_cycle()  # Send, Send, End -> Fire, Fire
l = list(spiking_engine.process_queue.queue)
assert type(l[0]) == QueueProcessNeuronFire and type(l[1]) == QueueProcessNeuronFire
spiking_engine.process_cycle()  # Fire, Fire, End -> Send, Send
l = list(spiking_engine.process_queue.queue)
assert type(l[0]) == QueueProcessNeuronSend and type(l[1]) == QueueProcessNeuronSend
spiking_engine.process_cycle()  # Send, Send, End -> Fire, Fire
l = list(spiking_engine.process_queue.queue)
assert type(l[0]) == QueueProcessNeuronFire and type(l[1]) == QueueProcessNeuronFire
spiking_engine.process_cycle()  # Fire, Fire, End -> Send, Send
spiking_engine.process_queue.get()
spiking_engine.process_queue.get()
assert spiking_engine.process_queue.qsize() == 0