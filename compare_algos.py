import networkx as nx
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime
from funcs import *
from statistics import mean 

def most_valuable_pages(p_r, tops_number = 10):
    
    p_r = (sorted(p_r, key = lambda item:item[1], reverse = True))
    print(p_r)
    nodes = []
    ranks = []
    for i in range(len(p_r)):
        nodes.append(p_r[i][0])
        ranks.append(p_r[i][1])
            
    nodes_classic = np.array(nodes[0:tops_number])
    ranks_classic = np.array(ranks[0:tops_number])
    lal = list(map(str, nodes_classic))
    bar_lab = [round(rank, 7) for rank in ranks_classic]
    title = "Топ " + str(tops_number) + " страниц с наибольшим значением ранга"
    
    my_colors = 'rgbkymc'
    f, ax = plt.subplots(figsize = (12, 8))
    br = plt.bar(nodes_classic, height = ranks_classic, width = 5, alpha = 0.5, color = my_colors, tick_label = lal)
    title = "Топ " + str(tops_number) + " страниц с наибольшим значением ранга"
    plt.xlabel("Номера страниц")
    plt.ylabel("Рейтинги страниц")
    plt.title(title)
    def autolabel(rects):
        for idx, rect in enumerate(br):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 0.5*height,
                    bar_lab[idx],
                    ha = 'center', va = 'bottom', rotation = 90)

    autolabel(br)

    plt.ylim(0,0.02)
    plt.show()
    return p_r

def find_not_right(PR_classic, PR_OPG):
    
    PR_classic = (sorted(PR_classic, key = lambda item:item[1], reverse = True))
    PR_OPG = (sorted(PR_OPG, key = lambda item:item[1], reverse = True))
    
    comp = []
    y1 = []
    y2 = []
    
    for i in range(len(PR_OPG)):
        if (PR_OPG[i][0] != PR_classic[i][0]):
            comp.append(1)
        y1.append(PR_OPG[i][0])  
        y2.append(PR_classic[i][0]) 
        
    plt.scatter(y1, y2, color = 'green', marker = 'o')
    plt.plot(y1, y1, color = 'red')
    plt.title('График несовпадения мест в рейтинге страниц')
    plt.show()
 
    print('Количество узлов с "неправильными" местами в рейтинге:', len(comp))
    
def plot_PR_values(PR_classic, PR_OPG):
    
    PR_classic_rates = []
    PR_OPG_rates = []
    PR_nodes = []
    
    for i in range(len(PR_classic)):
        PR_classic_rates.append(PR_classic[i][1])
        PR_OPG_rates.append(PR_OPG[i][1])
        PR_nodes.append(PR_classic[i][0])
    
    plt.plot(PR_nodes, PR_classic_rates, '-g', label = 'SciPy из NetworkX')
    plt.plot(PR_nodes, PR_OPG_rates, '--b', label = 'Метод ОПГ')
    plt.xlabel('Порядковый номер страницы')
    plt.ylabel('PageRank-значение')
    plt.title('PageRank в зависимости от номера узла')
    plt.show()
    
def time_compare(t):
    
      times = []
      for i in range(100):
        start = datetime.datetime.now()
        pg = pageranking()
        end = datetime.datetime.now()
        work_time1 = (end - start).total_seconds()
    
        start = datetime.datetime.now()
        pagerank = OPG_pagerank(t)
        end = datetime.datetime.now()
        work_time2 = (end - start).total_seconds()
        
        time_dif = work_time1 - work_time2
        times.append(time_dif)
    
      print("Время выполнения nx.pagerank_scipy():")
      print(work_time1, 'сек.')

      print("Время выполнения PageRank на ОПГ:")
      print(work_time2, 'сек.')
    
      print("Средняя разница во времени выполнения:")
      print(mean(times), 'сек.')
      return work_time1, work_time2, mean(times)