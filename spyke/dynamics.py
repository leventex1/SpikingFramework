from abc import ABC
from neuron import Synapse


class Counter:

    def __init__(self, offset: int = 0, step: int = 1) -> None:
        self.time_step = offset
        self.step = step

    def update(self) -> None:
        self.time_step += self.step

    def get_current_time_step(self) -> int:
        return self.time_step


class SynapticUpdater(ABC):

    def __init__(self) -> None:
        super().__init__()

    def update_synapse(self, synapse: Synapse) -> None:
        pass