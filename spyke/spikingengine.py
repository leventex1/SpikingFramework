import queue
from abc import ABC
from neuron import SpikingNeuron, Synapse


class QueueProcess(ABC):

    def __init__(self) -> None:
        super().__init__()

    def proceed(self) -> None:
        pass

    def is_process_cycle_finished(self) -> bool:
        pass


class QueueProcessCycleEnd(QueueProcess):

    def is_process_cycle_finished(self) -> bool:
        return True
    

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


class QueueProcessNeuronFire(QueueProcess):

    def __init__(self, fireing_neuron: SpikingNeuron, engine: 'SpikingEngine') -> None:
        self.fireing_neuron = fireing_neuron
        self.engine = engine
        super().__init__()

    def proceed(self) -> None:
        if not self.fireing_neuron.is_fireing():
            return
        
        self.fireing_neuron.reset_neuron()
        # On fireing
        self.engine.add_process(QueueProcessNeuronSend(self.fireing_neuron, self.engine))

    def is_process_cycle_finished(self) -> bool:
        return False


class SpikingEngine:

    def __init__(self) -> None:
        self.process_queue: queue.Queue[QueueProcess] = queue.Queue()

    def add_process(self, process: QueueProcess) -> None:
        self.process_queue.put(process)

    def process_cycle(self) -> None:

        self.add_process(QueueProcessCycleEnd())

        while True:
            process: QueueProcess = self.process_queue.get()

            if process.is_process_cycle_finished():
                break

            process.proceed()