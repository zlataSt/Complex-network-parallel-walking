"""Handler implementaion"""
from __future__ import annotations

from trajectory import Trajectory, MovedTrajectory
from typing import List, Callable
from node import Node
import values
from cache import CacheStruct


FIRST_NODE_MULTIPLIER = 0.1
REDUCE_MULTIPLIER = 0.25

class Handler:

    def __init__(self, first_node:Node, nodes_per_time:int, update:Callable, average:Callable, with_cache=False):
        self.blocked: bool = False
        self.nodes_per_time: int = nodes_per_time
        self.read_only: bool = False  # update the cache
        self.node: Node = first_node
        self.value = first_node.value * FIRST_NODE_MULTIPLIER
        self.sleep: int = 0  # skip the loop
        self._update: Callable = update
        self._average: Callable = average
        self.delete_after_trajectory: bool = False
        self.dumb_node: Node = Node(-1, 5, -1, 1)

        ## add to a tail cache
        if with_cache:
            c = CacheStruct(first_node, self)
            values.TAIL_CACHE.set(first_node.id, c)

    def merge(self) -> bool:
        """
        ----[HEAD]> [TAIL]------>
        result of merge
        ------[HEAD/TAIL]----->
        """
        cache = values.TAIL_CACHE.get(self.node.id)
        print(cache)
        if not cache:
            return False

        node = cache.value.node
        
        #sync values of nodes
        self.average_nodes(self.node, node)

        tail_trajectory = values.TRAJECTORIES[node.trajectory_id]
        head_trajectory = values.TRAJECTORIES[self.node.trajectory_id]
 
        if head_trajectory == tail_trajectory or head_trajectory.id == tail_trajectory.id:
            #print("Got the same trajectory in cache")
            return False

        # Create new trajectory
        merged_trajectory = head_trajectory.copy()
        merged_trajectory.merge(tail_trajectory)

        # place merged trajectory at tail trajectory
        values.TRAJECTORIES[head_trajectory.id] = merged_trajectory

        # Replace the tail trajectory with the old one
        trajectory_holder = MovedTrajectory(len(values.TRAJECTORIES)-1, len(head_trajectory)-1)
        values.TRAJECTORIES[node.trajectory_id] = trajectory_holder

        # Update current handler's values
        merged_trajectory.update_nodes_id()

        #print("AAAAAAAA")

        #remove from cash
        values.TAIL_CACHE._remove(cache)
        return True

    def exchange(self) -> bool:
        """
        Current handler is the first
        input:
        <a.tail>------x------<a.head>
        <b.tail>---x--------<b.head>
        output:
        <a.tail>-----x-----<b.tail>
        <b.tail>---x-----<a.head>
        """

        struct = values.CACHE.get_value(self.node.id)

        if not struct:
            return False
        
        second_handler = struct.handler
        
        if self.node.get_trajectory().id == second_handler.node.get_trajectory().id:
            #print("THE SAME TRAJECOTIRES %s" % self.node.get_trajectory().id)
            return False

        if self == second_handler:
            # TODO
            self._self_exchange(struct)
            return True
        # sync the values
        self.average_nodes(self.node, struct.node)

        values.COUNT_EXCHANGED += 1

        # update the trajectories 
        self.node.exchange(struct.node)

        first_copy = Handler(struct.node, self.nodes_per_time, self._update, self._average)
        # make sure the new handler wont overtake the current hanlder
        first_copy.sleep = 2
        self.value /= 2
        first_copy.value = self.value
        first_copy.delete_after_trajectory = True

        # the second 
        second_copy = Handler(
            self.node, second_handler.nodes_per_time, 
            second_handler._update, second_handler._average,
        )
        second_copy.sleep = 2
        second_copy.value = second_handler.value / 2
        second_copy.delete_after_trajectory = True

        values.HANDLERS.extend([first_copy, second_copy])
        return True

    def _self_exchange(self, struct: CacheStruct):
        pass

    def handle(self, nodes=None) -> None:
        if nodes is None:
            nodes = self.nodes_per_time
        if self.blocked:
            return
        if self.sleep:
            self.sleep -= 1
            return
        # iterate over loop
        for _ in range(nodes):

            # update the first node
            self.update_node()

            # If we have reached the end of a trajectory
            # Change the handler to blocked mode
            if self.node.is_last():
                # Call merge method
                merged = self.merge()
                # if we merged continue the loop
                if merged:
                    values.COUNT_MERGES += 1
                    continue
                # otherwise set block to true and exit handle
                self.blocked = True
                return

            exchanged = self.exchange()
            # Add a node only when there was no exchange
            if not exchanged:
                # Add node to cache
                struct = CacheStruct(self.node, self)
                values.CACHE.set(self.node.id, struct)
            
            n = self.node.get_next_node()
            if n is None:
                self.blocked = True
                return
            self.node = n

    def update_node(self) -> None:
        if self.read_only:
            # to keep the value of handler in read only mode as same as in update mode 
            self._update(self.dumb_node, self.value)
        else:
            self._update(self.node, self.value)

        #reduce handler's value
        self.value *= REDUCE_MULTIPLIER

    def _update_cache(self, trajectory: Trajectory) -> Node:
            node = trajectory[self.current_position]
            values.CACHE.set(node.id, self)
            self.current_position  += 1
            return node
    
    #### sync nodes in different trajectories 
    def average_nodes(self, first_node: Node, second_node: Node):
        self._average(first_node, second_node)

    def copy(self) -> Handler:
        copy = Handler(None, 0, sum, sum)
        copy.value = self.value
        copy.blocked = self.blocked
        return copy

    def start_new_trajectory(self, first_node: Node):
        self.blocked = False
        self.read_only = False
        self.node = first_node
        self.value = first_node.value * FIRST_NODE_MULTIPLIER
        c = CacheStruct(first_node, self)
        values.TAIL_CACHE.set(first_node.id, c)

    

if __name__ == "__main__":
    pass