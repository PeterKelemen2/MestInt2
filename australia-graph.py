import time

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def is_safe(graph, color, v, c):
    """
    A is_safe függvény ellenőrzi, hogy egy adott szín biztonságos-e egy adott csúcson.
    Ha a csúcsnak van olyan szomszédja, amelynek már ugyanaz a színe van mint a vizsgált színű csúcsnak akkor az nem biztonságos.
    """
    for i in range(len(graph)):
        if graph[v][i] and c == color[i]:
            return False
    return True


def is_consistent(graph, colors):
    """A is_safe függvény ellenőrzi, hogy a gráf színezése megfelelő-e.
    A függvény végig megy a gráf összes csúcsán és ellenőrzi,
    hogy van-e két szomszédos csúcs azonos színnel.
    Ha van, akkor a függvény hamis értékkel tér vissza, ha nincs akkor igaz értékkel."""
    for i in range(len(graph)):
        for j in range(i + 1, len(graph)):
            if graph[i][j] and colors[j] == colors[i]:
                return False
    return True


def backtracking_c(graph, colors, v, graf_colors, h=None):
    """függvény egy rekurzív függvény, ami megpróbálja megtalálni a gráf színezését c színnel.
    A függvény végig megy a gráf összes csúcsán és minden csúcsot megpróbál befesteni az c szín
    valamelyikével. Ha a gráf összes csúcsát befestette és az élkonzisztencia teljesül"""

    # Ha feldolgoztuk az összes csúcsot
    if v == len(graph):
        # Ha igaz akkor mindenhol tudtunk szinezni
        if h(graph, graf_colors):
            return True
        # Ha hamis akkor nem oldható meg a probléma
        else:
            return False

    # Rekurzívan bejárjuk a gráfot
    for j in range(0, colors):
        graf_colors[v] = j
        if backtracking_c(graph, colors, v + 1, graf_colors, h):
            return True
        graf_colors[v] = -1


def backtracking(graph, graf_colors, v, colors, h=None):
    """A graph_coloring_util függvény rekurzívan meghívja önmagát minden csúcsra és megpróbálja kiválasztani a színeket.
    Ha egy adott szín nem biztonságos (azaz ha már használják egy szomszédos csúcson), akkor kipróbál egy másik színt.
    Ha egyik szín sem biztonságos, akkor visszalép és megpróbálja újraszínezni az előző csúcsot."""

    # Megvizsgáljuk hogy melyik elemnél vagyzunk
    # ha 'v' == a gráf hosszával akkor készen vagyunk
    if v == len(graph):
        return True

    # Próbáljuk végig a szineket
    for c in range(colors):
        # Ha kiszinezhető a 'v' csúcs a 'c' színnel
        if h(graph, graf_colors, v, c):

            # színezzük ki a 'v' csúcsot 'c' színnel
            graf_colors[v] = c

            # szinezzük ki a következő csúcsot
            if backtracking(graph, graf_colors, v + 1, colors, h):
                return True

            # ha nem sikerül visszalépünk és az aktuálisan
            # kiszinezett csúcsot '-1'-re azaz szín nélkülire állítjuk
            graf_colors[v] = -1

    return False


start_time = time.time()
# Australia gráf
graph = [[0, 1, 1, 0, 0, 0],
         [1, 0, 1, 1, 0, 0],
         [1, 1, 0, 1, 1, 1],
         [0, 1, 1, 0, 1, 0],
         [0, 0, 1, 1, 0, 1],
         [0, 0, 1, 0, 1, 0]]

G = nx.Graph()
for i in range(len(graph)):
    for j in range(i + 1, len(graph)):
        if graph[i][j]:
            G.add_edge(i + 1, j + 1)

pos = nx.spring_layout(G)
# pos = nx.random_layout(G)
# pos = nx.arf_layout(G)
# pos = nx.shell_layout(G)
# pos = nx.planar_layout(G)
# pos = nx.spiral_layout(G)
# pos = nx.fruchterman_reingold_layout(G)

print(f"Elapsed time: {time.time() - start_time}")
# plt.show()

# Színezés:
# Mennyi színnel színezzünk
colors = 3
# Legyen -1 a szintelen
non_color = -1
# Hozzunk létre egy listát ami tartalmazza az egyes csúcsok színeit

graf_colors = [non_color] * len(graph)

# backtracking(graph, graf_colors, 0, colors, is_safe)
backtracking_c(graph, colors, 0, graf_colors, is_consistent)

if non_color not in graf_colors:
    print("A gráf színezése: ", graf_colors)
    color_dict = {
        0: "tab:red",
        1: "tab:blue",
        2: "tab:green"
    }
    nx.draw(G, pos, node_color=[color_dict[graf_colors[i]] for i in range(0, len(graf_colors))])
    nx.draw_networkx_labels(G, pos)
    plt.show()
else:
    print("Nem találtam megoldást a megadott színekkel.")
