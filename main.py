from collections import deque

from cups import Cup3
from hanoi import Hanoi
import problem
from node import Node
import numpy as np

from nqueens import NQueens


def depth_first_graph_search(problem):
    # print("Depth first graph search:")
    # Kezdő elem verembe helyezése
    frontier = [(Node(problem.initial))]
    # halmaz deklarálása a már bejárt elemekhez
    explored = set()

    steps = 0
    # Amig tudunk mélyebre menni
    while frontier:
        steps += 1
        # Legfelső elem kiemelése a veremből
        node = frontier.pop()

        # ha cél állapotban vagyunk vége
        if problem.goal_test(node.state):
            # print(f"{node.state}\n== Solution found in ({steps}) steps == \n")
            return node

        # állapot feljegyzése hogy tudjuk hogy már jártunk itt
        explored.add(node.state)

        # verem bővítése amig benemjárt elemekkel
        frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored and child not in frontier)
        # print(node.state)


def breadth_first_tree_search(problem):
    # print("Breadth first graph search:")
    # kezdő állapot kiolvasása és FIFO sorba helyezése
    frontier = deque([Node(problem.initial)])

    steps = 0
    # Amig nem értük el a határt
    while frontier:
        steps += 1
        # legszélsőbb elem kiemelése
        node = frontier.popleft()

        # ha cél állapotban vagyunk akkor vége
        if problem.goal_test(node.state):
            # print(f"{node.state}\n== Solution found in ({steps}) steps == \n")
            return node

        # A kiemelt elemből az összes új állapot legyártása az
        # operátorok segítségével
        frontier.extend(node.expand(problem))
        # print(node.state)


def trial_error(problem):
    """
    Próba hiba módszer
    """

    # kezdő állapot
    state = Node(problem.initial)

    steps = 0
    # végtelen ciklus definiálása
    while True:
        steps += 1
        # Ha a probléma megoldva akkor leállítjuk a végtelen ciklust
        if problem.goal_test(state.state):
            # print('Got it')
            return state, steps

        # Az alkalmazható operátorok segítsével
        # gyártsuk le az összes lehetséges utódot
        succesors = state.expand(problem)

        # Ha nincs új állapot (utód)
        if len(succesors) == 0:
            return 'Unsolvable'

        # random választunk egy újat a legyártott utódok közül
        state = succesors[np.random.randint(0, len(succesors))]
        # print(state.state)


def best_first_graph_search(problem, f):
    "A best-first kereső olyan keresőfával kereső, mely a legkisebb heurisztikájú nyílt csúcsot választja kiterjesztésre."

    # kezdő állapot létrehozása
    node = Node(problem.initial)
    # prioritásos (valamilyen heurisztika szerint rendezett) sor létrehozása
    frontier = []
    # kezdő állapot felvétele a prioritásos sorba
    frontier.append(node)
    # halmaz létrehozása a már megvizsgál elemekhez
    explored = set()

    # amíg találunk elemet
    while frontier:
        # elem kivétele a verem tetejéről
        node = frontier.pop()

        # ha cél állapotban vagyunk akkor kész
        if problem.goal_test(node.state):
            return node

        # feldolgozott elemek bővítése
        explored.add(node.state)

        # operátorral legyártott gyermek elemek bejárása
        for child in node.expand(problem):
            # ha még nem dolgoztuk fel
            if child.state not in explored and child not in frontier:
                frontier.append(child)

        # Rendezzük a listát (sort) a heurisztikának megfelelően
        frontier = f(frontier)
        print(node.state)


def astar_search(problem, f=None):
    """
    Az A*-algoritmus olyan A-algoritmusfajta, mely garantálja az optimális megoldás előállítását.
    h*(n) : az n -ből valamely célcsúcsba jutás optimális költsége.
    g*(n) : a startcsúcsból n -be jutás optimális költsége.
    f*(n)=g*(n)+h*(n) : értelemszerűen a startcsúcsból n -en keresztül valamely célcsúcsba jutás optimális költsége."""
    return best_first_graph_search(problem, f)


def sort_by_heur(items):
    """Válasszuk mindig a lehető legnagyobb indexű sort"""
    return sorted(items, key=lambda x: sum(x.state))


def main():
    # h = Hanoi(3)
    # print(f"Hanoi: {h.size}, {h.initial}, {h.goal}")
    # breadth_first_tree_search(h).solution()
    # depth_first_graph_search(h).solution()
    #
    # c = Cup3((5, 0, 0), [(4, 1, 0), (4, 0, 1)])
    # print(f"Hanoi: {c.initial}, {c.goal}")
    # breadth_first_tree_search(c).solution()
    # depth_first_graph_search(c).solution()
    #
    # # print(trial_error(c)[1])
    # t_error_sols = list()
    # tries = 100
    # for i in range(0, tries):
    #     t_error_sols.append(trial_error(c)[1])
    # # print(t_error_sols)
    # # print(sum(t_error_sols) / tries)

    nq = NQueens(4)
    print(nq.initial, nq.goal)
    print(astar_search(nq, sort_by_heur))
    # print(breadth_first_tree_search(nq).solution())
    # print(depth_first_graph_search(nq).solution())
    # print(trial_error(nq))

    # tmp = [Node((3, 2, -1, -1)), Node((3, -1, -1, -1)), Node((1, 2, -1, 0))]
    # print(sort_by_heur(tmp))


if __name__ == "__main__":
    main()
