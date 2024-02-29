import numpy as np

from node import Node


def hill_climbing(problem, heuristic):
    # kezdő állapot
    state = Node(problem.initial)

    # végtelen ciklus definiálása
    while True:
        # Ha a probléma megoldva akkor leállítjuk a végtelen ciklust
        if problem.goal_test(state.state):
            return state

        # Az alkalmazható operátorok segítsével
        # gyártsuk le az összes lehetséges utódot
        succesors = state.expand(problem)

        # keresünk egy jobb állapotott a heurisztikának megfelelően
        test_succesors = []
        for s_test in succesors:
            if heuristic(state.state) >= heuristic(s_test.state):
                test_succesors.append(s_test)

        # Ha nincs jobb állapot
        if len(test_succesors) == 0:
            return 'Unsolvable'

        # ha több azonosan jó van akkor random választunk egyet
        state = test_succesors[np.random.randint(0, len(test_succesors))]
        print(state.state)
