from random import choice as rchoice
from os import listdir
from typing import List

import pickle


def read_from_src_edgelist_to_idvalue():
    encounters = dict()
    #contacts = [[] for i in range(22657)]
    #src = open("src.twitterik", "r")
    contacts = [[] for i in range(380)]
    src = open("src.edgelist", "r")

    textik = src.readlines()

    for i in range(len(textik)):
        a = textik[i].rstrip("\n").split()
        textik[i] = a
        # print(textik[i])

        key1 = int(textik[i][0])
        key2 = int(textik[i][1])
        encounters[key1] = encounters.get(key1, 0) + 1
        encounters[key2] = encounters.get(key2, 0) + 1
        contacts[key1].append(key2)
        contacts[key2].append(key1)

    src.close()
    # print(encounters)

    pre = sorted(encounters.items(), key=lambda item: item[0])
    # print(type(pre), pre)
    res = []
    del contacts[0]
    for i in range(len(pre)):
        curr = list(pre[i]) + [contacts[i]]
        # print(curr)
        res.append(curr)

    return res


def id_value_dict():
    ids = read_from_src_edgelist_to_idvalue()
    return {id:value for (id, value, _) in ids}


def traverse(offset_start, source_graph):
    current_trajectory = set()
    next_index = offset_start - 1
    #print(f"next_number = {next_index + 1}")
    options = source_graph[next_index][2]
    #print(f"options = {options}")
    while not set(options).issubset(current_trajectory):
        current_trajectory.add(next_index + 1)
        next_index = rchoice(options) - 1
        #print(f"next_number = {next_index + 1}")
        options = source_graph[next_index][2]
        #print(f"options = {options}")
 
    if len(current_trajectory) < 3:
        current_trajectory = traverse(next_index, source_graph)
    return current_trajectory


def get_trajectories():
    test = read_from_src_edgelist_to_idvalue()
    unprocessed = set([i + 1 for i in range(len(test))])
    final = []

    while len(unprocessed) > 0:
        current = traverse(rchoice(list(unprocessed)), test)
        unprocessed.difference_update(current)
        # print(unprocessed)
        final.append(list(current))

    #print("final =", final)
    return final

# to prevent randomize output
# сохранение траекторий в файл
def save_trajectories(trajectories):
    dirs = listdir()
    version = 1
    while True:
        name = f'data_{version}.pickle'
        if name in dirs:
            version += 1
            continue
        with open(name, 'wb') as f:
            pickle.dump(trajectories, f)
        break

def load_trajectories_from_file(name) -> List[int]:
    with open(name, 'rb') as f:
        data = pickle.load(f)
    return data           

if __name__ == "__main__":
    ids = load_trajectories_from_file('data_1.pickle')