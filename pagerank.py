import networkx as nx

def pageranking():
    #graph = nx.read_edgelist("src.twitterik")
    graph = nx.read_edgelist("src.edgelist")
    page_ranks = list(nx.pagerank_scipy(graph).items())
    p_r = []
    for i in range(len(page_ranks)):
        p_r.append(list(page_ranks[i]))
        #print(type(p_r[i][0]))
        p_r[i][0] = int(p_r[i][0])
    page_ranks = sorted(p_r, key = lambda i:i[0], reverse = True)  
    return page_ranks

if __name__ == "__main__":
    pageranking()
