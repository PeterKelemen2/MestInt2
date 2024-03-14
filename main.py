from collections import deque

from cups import Cup3
from hanoi import Hanoi
import problem
from node import Node


def depth_first_graph_search(problem):
    print("Depth first graph search:")
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
            print(f"{node.state}\n== Solution found in ({steps}) steps == \n")
            return node

        # állapot feljegyzése hogy tudjuk hogy már jártunk itt
        explored.add(node.state)

        # verem bővítése amig benemjárt elemekkel
        frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored and child not in frontier)
        print(node.state)


def breadth_first_tree_search(problem):
    print("Breadth first graph search:")
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
            print(f"{node.state}\n== Solution found in ({steps}) steps == \n")
            return node

        # A kiemelt elemből az összes új állapot legyártása az
        # operátorok segítségével
        frontier.extend(node.expand(problem))
        print(node.state)


def main():
    h = Hanoi(3)
    print(f"Hanoi: {h.size}, {h.initial}, {h.goal}")
    breadth_first_tree_search(h).solution()
    depth_first_graph_search(h).solution()

    c = Cup3((5, 0, 0), [(4, 1, 0), (4, 0, 1)])
    print(f"Hanoi: {c.initial}, {c.goal}")
    breadth_first_tree_search(c).solution()
    depth_first_graph_search(c).solution()


if __name__ == "__main__":
    main()
