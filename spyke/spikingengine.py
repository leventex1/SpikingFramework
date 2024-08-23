import queue
from abc import ABC
from spyke.neuron import SpikingNeuron, Synapse
from spyke.dynamics import Counter


class QueueProcess(ABC):

    def __init__(self) -> None:
        super().__init__()

    def proceed(self) -> None:
        pass

    def is_process_cycle_finished(self) -> bool:
        pass

    def __str__(self) -> str:
        pass


class QueueProcessCycleEnd(QueueProcess):

    def is_process_cycle_finished(self) -> bool:
        return True
    
    def __str__(self) -> str:
        return 'end'
    

class QueueProcessNeuronSend(QueueProcess):

    def __init__(self, sending_neuron: SpikingNeuron, engine: 'SpikingEngine') -> None:
        self.sending_neuron = sending_neuron
        self.engine = engine
        super().__init__()

    def proceed(self) -> None:
        for connection in self.sending_neuron.connections:
            post_node: SpikingNeuron = connection.end_node
            synapse: Synapse = connection

            post_node.change_membrane_value(synapse.weight)
            if post_node.is_fireing():
                self.engine.add_process(QueueProcessNeuronFire(post_node, self.engine))

    def is_process_cycle_finished(self) -> bool:
        return False
    
    def __str__(self) -> str:
        return f'send({self.sending_neuron.id})'


class QueueProcessNeuronFire(QueueProcess):

    def __init__(self, fireing_neuron: SpikingNeuron, engine: 'SpikingEngine') -> None:
        self.fireing_neuron = fireing_neuron
        self.engine = engine
        super().__init__()

    def proceed(self) -> None:
        if not self.fireing_neuron.is_fireing():
            return
        
        self.fireing_neuron.reset_neuron()
        self.fireing_neuron.on_fireing()
        self.engine.add_process(QueueProcessNeuronSend(self.fireing_neuron, self.engine))

    def is_process_cycle_finished(self) -> bool:
        return False
    
    def __str__(self) -> str:
        return f'fire({self.fireing_neuron.id})'


class SpikingEngine:
    """
    SpikingEngine is the graph implementing the spiking neural network 'spinner' algorithm.
    
    member variables:
    - self.process_queue: Queue[QueueProcess], helper container for the dfs treversial.
    - self.counter: Counter, updates every time the process_cycle is called.

    methods:
    - add_process(self, process: QueueProcess) -> None, adds a QueueProcess to the self.process_queue.
    - process_cycle(self) -> None, adds an EndProcess to the self.process_queue and processes it while the EndProcess is hit.
        Suppose the spiking neural network is a graph than if there are fire processes in the queue than the graph is treversed on the edges but only for a distance of 1. 
    """

    def __init__(self, counter: Counter) -> None:
        self.process_queue: queue.Queue[QueueProcess] = queue.Queue()
        self.counter = counter

    def add_process(self, process: QueueProcess) -> None:
        self.process_queue.put(process)

    def process_cycle(self) -> None:

        self.add_process(QueueProcessCycleEnd())

        while True:
            process: QueueProcess = self.process_queue.get()

            if process.is_process_cycle_finished():
                break

            process.proceed()

        self.counter.update()