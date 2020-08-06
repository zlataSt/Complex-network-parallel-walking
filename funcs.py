""" Update and average implementation."""
import networkx as nx
import operator
from node import Node

def first_average(firs_node: Node, second_node: Node):
    mean = (firs_node.value + second_node.value) / 2
    firs_node.value, second_node.value = mean, mean

def first_update(node: Node, value: float):
    node.value += value

def pageranking():
    graph = nx.read_edgelist("src.edgelist")
    page_ranks = list(nx.pagerank_scipy(graph).items())
    p_r = []
    for i in range(len(page_ranks)):
        p_r.append(list(page_ranks[i]))
        #print(type(p_r[i][0]))
        p_r[i][0] = int(p_r[i][0])
    page_ranks = sorted(p_r, key = lambda i:i[0], reverse = True)  
    return page_ranks

def OPG_pagerank(trajectories):
    nod = {}
    for nodes in trajectories:
        #print(nodes)
        for node in nodes:
            #print(node)
            if node.id in nod:
                # меняем значение узла
                # а также увеличиваем частоту появления во множестве траекторий
                # если уже рассматривали данный узел
                nod[node.id] = [nod[node.id][0] + node.value, nod[node.id][1] + 1]
            else:
                # если рассматриваем узел впервые,
                # то добавляем его в nod
                nod[node.id] = [node.value, 1]
    
    total_n = 0
    
    for i in node.keys():
        # вычисляем для каждого узла его итоговое среднее значение
         node[i] = node[i][0] / node[i][1]
         # и сумму средних значений всех узлов
         total_n = total_n + node[i]
    
    for i in node.keys():
        # значение PageRank для i-го узла:
        node[i] = node[i]/total_n
       
    # сортировка по ключу
    so = sorted(n.items(), key = operator.itemgetter(0), reverse = True)
    pages = []
    for i in range(len(res)):
        pages.append(list(so[i]))
        
    return pages

def pagerank_deviations(OPG_pagerank):
    
    errors = []
    true_pr = pageranking()
    
    for i in range(len(true_pr)):
        errors.append([true_pr[i][0], (true_pr[i][1] - OPG_pagerank[i][1])])
      
    MAE = 0
    MSE = 0
    for i in errors:
        MAE = MAE + abs(i[1])
        MSE = MSE + i[1]**2
    MAE = MAE/len(errors)
    MSE = MSE/len(errors)
    print('Сравнение ОПГ ')
    print('Средняя абсолютная ошибка:')
    print(MAE)
    print('Среднеквадратичная ошибка:')
    print(MSE)
    return MAE, MSE
