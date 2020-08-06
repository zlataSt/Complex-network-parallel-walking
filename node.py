"""Node implementation."""
from __future__ import annotations

from typing import List
import values
from typing import Union

class Node:
    """Node."""
    
    def __init__(self, id: int, value: float, trajectory_id: int, index:int, params: list = []):
        self.id: int = id
        self.value: float = value
        self.params: list = params
        self.trajectory_id: int = trajectory_id
        self.index: int = index # index in trajectory's list
        

    def update_value(self, value):
        #TODO calculation of value
        self.value += value

    def get_next_node(self) -> Union[Node, None]:
        trajectory = values.TRAJECTORIES[self.trajectory_id]
        if len(trajectory) - 1 <= self.index:
            return None
        return trajectory[self.index + 1]

    # получение траектории из множества траекторий по ее идентификатору
    def get_trajectory(self):
        return values.TRAJECTORIES[self.trajectory_id]

    def exchange(self, node: Node):
        curr_trajectory = self.get_trajectory()
        their_trajectory = node.get_trajectory()
        curr_trajectory.exchange(their_trajectory, self.index, node.index)
        
    # проверка на "хвостовой" узел
    def is_last(self) -> bool:
        return values.TRAJECTORIES[self.trajectory_id][-1] == self

    def __str__(self) -> str:
        return 'Node id: %s, value: %s, trajectory_id: %s index: %s' % (self.id, self.value, self.trajectory_id, self.index)