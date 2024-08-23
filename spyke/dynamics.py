from abc import ABC
import math
from spyke.neuron import Synapse


class Counter:

    def __init__(self, offset: float = 0, step: float = 1) -> None:
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
        if synapse.pre_fire_time_step is None or synapse.post_fire_time_step is None:
            return
        
        dt = synapse.post_fire_time_step - synapse.pre_fire_time_step
        synapse.set_post_fire_time_step(None)
        synapse.set_pre_fire_time_step(None)

        if dt == 0:
            return
        synapse.weight += 0.01 * math.exp(-dt) if dt > 0 else -0.01 * math.exp(dt)

        if synapse.weight < 0:
            synapse.weight = 0
        if synapse.weight > 1:
            synapse.weight = 1