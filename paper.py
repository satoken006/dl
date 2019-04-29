# -*- Coding: utf-8 -*-

import urllib.request, urllib.error
from bs4 import BeautifulSoup
import networkx as nx
import collections
import itertools
import matplotlib.pyplot as plt

from const import MEMBERS, MEMBERS_EN


node_size = {}
edge_list = []
PAPER_MAX = 146

for i in range(1, PAPER_MAX):
    try:
        html = urllib.request.urlopen("http://dl.nkmr-lab.org/papers/"+str(i))
        print(str(i) + " / " + str(PAPER_MAX))
    except urllib.error.HTTPError as e:
        continue
    except NameError as e:
        continue

    soup = BeautifulSoup(html, "lxml")

    titleElem = soup.find("h1")
    title = titleElem.get_text()
    print(title)
    divElem = titleElem.parent
    a_list = divElem.find_all("a")
    

    main_author = a_list[0].get_text(" ", strip=True)

    if main_author in MEMBERS.keys():
        main_author = MEMBERS[main_author]

        if main_author in node_size:
            node_size[main_author] += 1
        else:
            node_size[main_author] = 1

    elif main_author in MEMBERS_EN.keys():
        main_author = MEMBERS_EN[main_author]

        if main_author in node_size:
            node_size[main_author] += 1
        else:
            node_size[main_author] = 1

    else:
        continue
    

    for i in range(1, len(a_list)):
        co_author = a_list[i].get_text(" ", strip=True)
        if co_author in MEMBERS.keys():
            co_author = MEMBERS[co_author]
        elif co_author in MEMBERS_EN.keys():
            co_author = MEMBERS_EN[co_author]
        else:
            continue
        
        if co_author != "PDF":
            print(co_author + " --> " + main_author)
            edge_list.append([co_author, main_author])

print( node_size )
# print(edge_list)


edge_count = collections.Counter(itertools.chain.from_iterable(edge_list)).most_common(100)
G = nx.DiGraph()
# G.add_nodes_from([(edge, {"count":count}) for edge,count in edge_count])
G.add_nodes_from([(edge, {"size":11}) for edge,count in edge_count])

for edge in edge_list:
    for node0,node1 in itertools.combinations(edge, 2):
        if not G.has_node(node0) or not G.has_node(node1):
            continue
        if G.has_edge(node0, node1):
            G.edge[node0][node1]["weight"] += 1
        else:
            G.add_edge(node0, node1, {"weight":1})

# set labels of nodes anonymous
# start = 1
# G = nx.convert_node_labels_to_integers(G,first_label=start)

# G.node_attr['width'] = '0.25'
# G.node_attr['height'] = '0.25'

#pos = nx.spring_layout(G, k=0.6)
# edge_width = [ d["weight"] for (u,v,d) in G.edges(data=True)]
# nx.draw_networkx(G,pos, width=edge_width) # draw graph with networkx
nx.nx_agraph.view_pygraphviz(G, prog='fdp') # draw graph with pygraphviz

plt.figure(figsize=(15,15))
plt.axis("off")
plt.show()