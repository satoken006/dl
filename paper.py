# -*- Coding: utf-8 -*-

import urllib.request, urllib.error
from bs4 import BeautifulSoup
import networkx as nx
import collections
import itertools
import matplotlib.pyplot as plt

from const import MEMBERS, MEMBERS_EN
from RepositoryParser import RepositoryParser

parser = RepositoryParser()
edge_list = []
RANGE = 146

for i in range(1, RANGE + 1):
    # Connect to the Web and get HTML
    try:
        html = urllib.request.urlopen("http://dl.nkmr-lab.org/papers/"+str(i))
        print(str(i) + " / " + str(RANGE))
    except urllib.error.HTTPError as e:
        continue
    except NameError as e:
        continue

    soup = BeautifulSoup(html, "lxml")

    # Get a main author and co-authors
    author_list = parser.get_author_list(soup)
    main_author = author_list[0].get_text(" ", strip=True)

    if main_author in MEMBERS.keys():
        main_author = MEMBERS[main_author]
    elif main_author in MEMBERS_EN.keys():
        main_author = MEMBERS_EN[main_author]
    else:
        continue

    for i in range(1, len(author_list)):
        co_author = author_list[i].get_text(" ", strip=True)

        if co_author in MEMBERS.keys():
            co_author = MEMBERS[co_author]
        elif co_author in MEMBERS_EN.keys():
            co_author = MEMBERS_EN[co_author]
        else:
            continue
        
        if co_author != "PDF":
            print(co_author + " --> " + main_author)
            edge_list.append([co_author, main_author])

edge_count = collections.Counter(itertools.chain.from_iterable(edge_list)).most_common(100)
G = nx.DiGraph()
# G.add_nodes_from([(edge, {"count":count}) for edge,count in edge_count])
G.add_nodes_from([(edge, {"size":11}) for edge,count in edge_count])

for edge in edge_list:
    for node0,node1 in itertools.combinations(edge, 2):
        if not G.has_node(node0) or not G.has_node(node1):
            continue


        G.add_weighted_edges_from([(node0, node1, 1)])
        # if G.has_edge(node0, node1):
        #     # print(node0, node1, G[node0][node1])
        #     G[node0][node1]["weight"] += 1
        # else:

# draw graph with pygraphviz
nx.nx_agraph.view_pygraphviz(G, prog='fdp')

plt.figure(figsize=(15,15))
plt.axis("off")
plt.show()