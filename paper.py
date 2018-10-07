# -*- Coding: utf-8 -*-

import urllib.request, urllib.error
from bs4 import BeautifulSoup
import networkx as nx
import collections
import itertools
import matplotlib.pyplot as plt

from const import MEMBERS, MEMBERS_EN


edge_list = []

for i in range(1, 107):
    try:
        html = urllib.request.urlopen("http://dl.nkmr-lab.org/papers/"+str(i))
    except urllib.error.HTTPError as e:
        continue
    except NameError as e:
        continue

    soup = BeautifulSoup(html)
    # print( soup )

    title = soup.find("h1").get_text()
    print( title )

    div = soup.find("div")
    div2 = div.find_all("div")[1]
    div3 = div2.find("div") 
    div4 = div3.find_all("div", recursive=False)[0]
    div5 = div4.find("div")
    header = div5.find("header")
    a_list = header.find_all("a")

    main_author = a_list[0].get_text(" ", strip=True)
    if main_author in MEMBERS.keys():
        main_author = MEMBERS[main_author]
    elif main_author in MEMBERS_EN.keys():
        main_author = MEMBERS_EN[main_author]
    else:
        continue
    

    for i in range(1, len(a_list)):
        co_author = a_list[i].get_text(" ", strip=True)
        if co_author in MEMBERS.keys():
            co_author = MEMBERS[co_author]
        elif co_author in MEMBERS_EN.keys():
            co_author = MEMBERS_EN[co_author]
        else:
            print()
            continue
        
        if co_author != "PDF":
            print(co_author + " --> " + main_author)
            edge_list.append([co_author, main_author])
    print()

# print(edge_list)


edge_count = collections.Counter(itertools.chain.from_iterable(edge_list)).most_common(100)
G = nx.DiGraph()
G.add_nodes_from([(edge, {"count":count}) for edge,count in edge_count])

for edge in edge_list:
    for node0,node1 in itertools.combinations(edge, 2):
        if not G.has_node(node0) or not G.has_node(node1):
            continue
        if G.has_edge(node0, node1):
            G.edge[node0][node1]["weight"] += 1
        else:
            G.add_edge(node0, node1, {"weight":1})

# set anonymous
# start = 1
# G = nx.convert_node_labels_to_integers(G,first_label=start)

#pos = nx.spring_layout(G, k=0.6)
edge_width = [ d["weight"] for (u,v,d) in G.edges(data=True)]
# nx.draw_networkx(G,pos, width=edge_width) # draw graph with networkx
nx.nx_agraph.view_pygraphviz(G, prog='fdp') # draw graph with pygraphviz

plt.figure(figsize=(15,15))
plt.axis("off")
plt.show()