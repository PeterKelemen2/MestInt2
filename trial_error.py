from node import Node
import numpy as np


def trial_error(problem):
    """
    Próba hiba módszer
    """

    # kezdő állapot
    state = Node(problem.initial)

    # végtelen ciklus definiálása
    while True:
        # Ha a probléma megoldva akkor leállítjuk a végtelen ciklust
        if problem.goal_test(state.state):
            print('Got it')
            return state

        # Az alkalmazható operátorok segítsével
        # gyártsuk le az összes lehetséges utódot
        succesors = state.expand(problem)

        # Ha nincs új állapot (utód)
        if len(succesors) == 0:
            return 'Unsolvable'

        # random választunk egy újat a legyártott utódok közül
        state = succesors[np.random.randint(0, len(succesors))]
        print(state.state)
