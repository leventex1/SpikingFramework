from abc import ABC
from typing import Callable
from spyke.connection import Node, Connection


class Neuron(ABC, Node):
    """
    Neuron class is the base implementation of a digital artificial neuron.
    This class can be extended to behave differently with all kind of neural networks, like SNN or simple ANN.

    static variables:
    - ID: int, keep track of the newly created neuron's id.

    member variables:
    - self.resert_value: float, the value where the membrane_value will be reseted after calling self.reset_neuron().
    - self.membrane_value: float, holds the neuron's membrane "potential" value.
    - self.id: int, a unique id that identifies the neuron, for debug purposes.
    - self.on_fireing_callback: None | (neuron: Neuron) -> None, is a callback function that should be called when the self.on_fireing is called.
    - self.on_before_membrane_change_callback: None | (neuron: Neuron, time_step: int) -> None, is a callback that should be called before self.change_membrane_value(...) is called.

    methods:
    - get_membrane_value(self) -> float, getter for membrane_value member variable.
    - change_membrane_value(self, change: float) -> None, changes the membrane_value with change.
    - reset_neuron(self) -> None, set the self.membrane_value to the self.resert_value.
    - is_fireing(self) -> bool, is an abstract method, should return if the neuron is fireing or not. Like in simple artificial neurons it's always True, whereas in spiking neurons it's either True of False.
    - on_fireing(self) -> None, should be called in protocols when the neuron is fireing. The self.on_fireing_callback(neuron: Neuron) -> None, is called.
    - on_before_membrane_change_callback(self, time_step: int) -> None, should be called in protocols before a neuron's membrane potential is changed, so before .change_membrane_potential.
    """
    ID: int = 0

    def __init__(self,
            reset_value: float, 
            membrane_value: float,
            on_fireing_callback: None | Callable[['Neuron'], None],
            on_before_membrane_change_callback: None | Callable[['Neuron', int], None]) -> None:
        super().__init__()
        self.reset_value: float = reset_value
        self.membrane_value: float = membrane_value
        self.id: int = SpikingNeuron.ID
        SpikingNeuron.ID += 1

        self.on_fireing_callback: None | Callable[[Neuron], None] = on_fireing_callback
        self.on_before_membrane_change_callback: None | Callable[[Neuron, int], None] = on_before_membrane_change_callback

    def get_membrane_value(self) -> float:
        return self.membrane_value
    
    def on_before_membrane_change(self, time_step: int) -> None:
        self.on_before_membrane_change_callback and self.on_before_membrane_change_callback(self, time_step)

    def change_membrane_value(self, change: float) -> None:
        self.membrane_value += change
    
    def reset_neuron(self) -> None:
        self.membrane_value = self.reset_value

    def on_fireing(self) -> None:
        self.on_fireing_callback and self.on_fireing_callback(self)

    def is_fireing(self) -> bool:
        pass


class SpikingNeuron(Neuron):
    """
    SpikingNeuron inherits the Neuron class.
    
    member variables:
    - self.threshold_value: float, indicates the spiking neurons membrane threshold value where the neuron fires.
    - self.last_updated_time_step: None | int, keeps track when the neuron is last updated. Helper variables for some attached dynamics.

    methods:
    - is_fireing(self) -> bool, returns True if the membrane_value is ">=" the threshold_value, otherwise returns False.
    """

    def __init__(self, 
        reset_value: float = 0.0, 
        membrane_value: float = 0.0, 
        threshold_value: float = 1.0,
        on_fireing_callback: None | Callable[['SpikingNeuron'], None] = None,
        on_before_membrane_change_callback: None | Callable[['SpikingNeuron', int], None] = None) -> None:
        super().__init__(reset_value, membrane_value, on_fireing_callback, on_before_membrane_change_callback)
        self.threshold_value: float = threshold_value
        self.last_updated_time_step: None | int = None

    def is_fireing(self) -> bool:
        return self.membrane_value >= self.threshold_value
    

class Synapse(Connection):
    """
    Synapse is the child of Connection.
    Holds the synaptic weight and the time when the pre and post neurons last spiked.

    member variables:
    - self.weight: float
    - self.pre_fire_time_step: int | None, last pre node spike time.
    - self.post_fire_time_step: int | None, last post node spike time.

    methods:
    - set_pre_fire_time_step(self, time_step: int) -> None, sets the pre node time step.
    - set_post_fire_time_step(self, time_step: int) -> None, sets the post node time step.
    """

    def __init__(self, weight: float, post_neuron: SpikingNeuron) -> None:
        super().__init__(post_neuron)
        self.weight = weight
        self.pre_fire_time_step: int | None = None
        self.post_fire_time_step: int | None = None

    def set_pre_fire_time_step(self, time_step: int | None) -> None:
        self.pre_fire_time_step = time_step

    def set_post_fire_time_step(self, time_step: int | None) -> None:
        self.post_fire_time_step = time_step