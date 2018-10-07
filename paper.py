# -*- Coding: utf-8 -*-

import urllib.request, urllib.error
from bs4 import BeautifulSoup
import networkx as nx
import collections
import itertools
import matplotlib.pyplot as plt

from const import members


edge_list = []


for i in range(1,107):
    try:
        html = urllib.request.urlopen("http://dl.nkmr-lab.org/papers/"+str(i))
    except urllib.error.HTTPError as e:
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
    a_list = header.find_all("a");

    main_author = a_list[0].get_text(" ", strip=True)
    if not main_author in members.keys():
        continue
    main_author = members[main_author]

    for i in range(1, len(a_list)):
        co_author = a_list[i].get_text(" ", strip=True)
        if not co_author in members.keys():
            continue
        co_author = members[co_author]

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


plt.figure(figsize=(15,15))
pos = nx.spring_layout(G, k=0.3)

edge_width = [ d["weight"] for (u,v,d) in G.edges(data=True)]
# nx.draw_networkx(G,pos, width=edge_width) # 無向グラフ
nx.nx_agraph.view_pygraphviz(G, prog='fdp') # pygraphvizによる有向グラフ

plt.axis("off")
plt.show()
