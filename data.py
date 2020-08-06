from typing import List
from node import Node
from trajectory import Trajectory
from trajectory_dumb import load_trajectories_from_file, id_value_dict



def load_trajectories(file_name: str) -> List[Trajectory]:

    # create trajectories
    ids = load_trajectories_from_file(file_name)
    values = id_value_dict()
    out: List[Trajectory] = []
    # Create nodes
    # trajectory_id = index
    for i in range(len(ids)):
        nodes = [Node(id=id, value=values.get(id), trajectory_id=i, index=index) \
                for index, id in enumerate(ids[i])]
        out.append(Trajectory(id=i, nodes=nodes))    
    return out


if __name__ == "__main__":
    for i in load_trajectories("data_1.pickle"):
        for j in i:
            print(j)