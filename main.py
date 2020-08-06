"""Main loop"""
import datetime
import os
#import math

import values
from handler import Handler
from typing import List
from data import load_trajectories
from funcs import *
from trajectory import Trajectory
from compare_algos import *
from statistics import mean 


HANDLERS_COUNT: int = os.getenv("HANDLERS_COUNT", 10)
PICKLED_TRAJECTORIES_FILE: str = os.getenv("PICKLED_TRAJECTORIEs_FILE", "data_1.pickle")
NODES_PER_TIME: int = os.getenv("NODES_PER_TIME", 3)
CURRENT_UNHANDLER_TRAJECTORY = 0


def main():
    
    global CURRENT_UNHANDLER_TRAJECTORY
    values.TRAJECTORIES = load_trajectories(PICKLED_TRAJECTORIES_FILE)


    for i in range(HANDLERS_COUNT):
        values.HANDLERS.append(
            Handler(
                first_node= values.TRAJECTORIES[i].get_first_node(), 
                nodes_per_time=NODES_PER_TIME, 
                update=first_update,
                average=first_average,
                with_cache=True,
                ),
            )
        values.TRAJECTORIES[i].is_handled = True
        CURRENT_UNHANDLER_TRAJECTORY += 1
    
    ## main loop
    #print("trajectories before %s" % len(values.TRAJECTORIES))
    for k in range(100):
        i = 0
        while i < len(values.HANDLERS):
            h: Handler = values.HANDLERS[i]
            h.handle()
            i += 1

        # filter out the hanlders you need to delete after handling a trajectory
        values.HANDLERS = list(filter(lambda x: not x.delete_after_trajectory, values.HANDLERS))

        for i in values.HANDLERS:
            if i.blocked and CURRENT_UNHANDLER_TRAJECTORY < len(values.TRAJECTORIES):
                i.start_new_trajectory(values.TRAJECTORIES[CURRENT_UNHANDLER_TRAJECTORY].get_first_node())
                CURRENT_UNHANDLER_TRAJECTORY += 1

    cnt = 0
    for i in values.TRAJECTORIES:
        if type(i) is Trajectory:
            cnt += 1

    t = filter(lambda x: type(x) is Trajectory, values.TRAJECTORIES)
    
    #times = []
    
    # двумерные списки вида [номер узла, ранжированный вес узла]
    pg = pageranking()
    pagerank = OPG_pagerank(t)
    
    # отклонения в значениях, вычисленных двумя методами
    pagerank_deviations(pagerank)
    
    # топ-n страниц (узлов) по значению весов
    # рисует график
    most_valuable_pages(pagerank)
    
    # визуализация мест в "рейтингах" всех узлов
    # вычисленных двумя способами
    find_not_right(pg, pagerank)
    
    # ранг в зависимости от номера узла
    plot_PR_values(pg, pagerank)
    
    time_compare(t)

if __name__ == "__main__":
    main()