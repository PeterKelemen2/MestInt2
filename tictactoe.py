import numpy as np

from game import Game
from collections import namedtuple
import random

GameState = namedtuple("GameState", "to_move, utility, board, moves")


class TicTacToe(Game):
    """Egy TicTacToe játék rendelkezik egy táblával. Az első játékos X-el lép míg
    a második játékos O-val. A játék tárolja a játékosok lépéseit."""

    def __init__(self, h=3, v=3, k=3):
        """TicTacToe konstruktor. Feladata a játék kezdő állapotának megadása."""
        self.h = h  # sorok száma
        self.v = v  # oszlopok száma
        self.k = k  # hány egymást követő X-re vagy O-ra van szükség egy sorban, oszlopban vagy átlósan a győzelemhez
        moves = [(x, y) for x in range(1, h + 1) for y in
                 range(1, v + 1)]  # A kezdőállapotból elérhető összes lehetséges mozgás
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)  # kezdő állapot beállítása

    def actions(self, state):
        """A lehetséges lépések. Valójában minden olyan mező amit még nem foglaltak el"""
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state  # Mert Illegális lépést nem tehetünk!

        # készítünk egy másolatot a táblára
        board = state.board.copy()

        # A táblára beállítjuk az új lépést. Tehát X vagy O
        board[move] = state.to_move

        # Frissítsük a lehetséges lépések listáját úgy, hogy
        # töröljük belőle a megtett lépést
        moves = list(state.moves)
        moves.remove(move)

        # Állítsuk elő az új állapotot
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        """Visszaadja az értéket a játékosnak; 1 a győzelemért, -1 a vereségért, 0 egyébként."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """Egy állapot akkor végső, ha nyert, vagy nincsenek üres mezők."""
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        # Kérjük le a táblát. Ami egy "dic" (szótár) objektum
        board = state.board

        # Járjuk be a táblát
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                # Írjuk ki az értékét ha van olyan eleme a szótárnak (táblának) ha nincs
                # akkor írjunk ki egy pontot
                print(board.get((x, y), '.'), end=' ')
            print()
        print()

    def compute_utility(self, board, move, player):
        """Ha 'X' nyer ezzel a lépéssel, adjon vissza 1-et; ha 'O' nyer, akkor -1; különben vissza 0."""
        if (self.k_in_row(board, move, player, (0, 1)) or  # oszlopok ellenőrzése
                self.k_in_row(board, move, player, (1, 0)) or  # sorok ellenőrzése
                self.k_in_row(board, move, player, (1, -1)) or  # / - átló ellenőrzése
                self.k_in_row(board, move, player, (1, 1))):  # \ - átló ellenőrzése
            return +1 if player == 'X' else -1
        else:
            return 0

    def k_in_row(self, board, move, player, delta_x_y):
        """Vissza ad egy igaz értéket ha az adott irányba a játékos kigyűjtötte a megfelelő
        mennyiségű elemet."""
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n a lépések száma a sorban 
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Mert magát a mozgást kétszer számoltuk
        return n >= self.k


def random_player(game, state):
    """A random játékos választ véletleszerűen egyet a lehetséges lépések közül."""
    return random.choice(game.actions(state)) if game.actions(state) else None


def minmax(state, game):
    """Min-max döntés alapján működő keresés implementációja"""

    # Játékos szabad lépéseinek lekérdezése. Hova léphet?
    player = game.to_move(state)

    def max_value(state):
        # ha játék végállás akkor vissza adjuk az eredményt
        if game.terminal_test(state):
            return game.utility(state, player)

        v = -np.inf
        # Vissza adjuk a minimum értékek közül a legnagyobbat
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))

        return v

    def min_value(state):
        # ha játék végállás akkor vissza adjuk az eredményt
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        # Vissza adjuk a maximum értékek közül a legkisebbet
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        return v

    # MinMax rekurziv lánc hívás. A gyökér maximumból indul tehát az
    # ő gyermekinek a minimum elemek lesznek amely minimu elemek gyermekei pedig maximumok
    # Ez a bejárás pedig a max_value és min_value függvények segítségével meg fog történi.
    return max(game.actions(state), key=lambda a: min_value(game.result(state, a)))


def minmax_player(game, state):
    """Min-max algoritmus alapján lépést választó játékos"""
    return minmax(state, game)


def alpha_beta_player(game, state):
    return alpha_beta_search(state, game)


def alpha_beta_search(state, game):
    """Alfa-béta vágás alapján működő keresés implementációja"""

    # Játékos szabad lépéseinek lekérdezése. Hova léphet?
    player = game.to_move(state)

    def max_value(state, alpha, beta):
        # ha játék végállás akkor vissza adjuk az eredményt
        if game.terminal_test(state):
            return game.utility(state, player)

        v = -np.inf
        # Lehetséges lépések alkalmazása
        for a in game.actions(state):
            # Maximum meghatározása
            v = max(v, min_value(game.result(state, a), alpha, beta))
            # Ha nagyobb mint az eddigi beta akkor vissza adjuk
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        # ha játék végállás akkor vissza adjuk az eredményt
        if game.terminal_test(state):
            return game.utility(state, player)

        v = np.inf
        # Lehetséges lépések alkalmazása
        for a in game.actions(state):
            # Minimum meghatározása
            v = min(v, max_value(game.result(state, a), alpha, beta))
            # Ha kisebb mint az eddigi alfa akkor vissza adjuk
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Alfa-beta keresés:
    # legjobb eredméy
    best_score = -np.inf
    # beta értéke
    beta = np.inf
    # legjobb lépés
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta)
        if v > best_score:
            best_score = v
            best_action = a

    return best_action


def main():
    ttt = TicTacToe()
    print("Initial state:")
    ttt.display(ttt.initial)

    GameState = namedtuple('GameState', 'to_move, utility, board, moves')

    my_state = GameState(to_move='X',
                         utility='0',
                         board={(1, 1): 'X', (1, 2): 'O', (1, 3): 'X',
                                (2, 1): 'O', (2, 3): 'O',
                                (3, 1): 'X'},
                         moves=[(2, 2), (3, 2), (3, 3)])

    # print("State:")
    # ttt.display(my_state)

    # random_player(ttt, my_state)
    # minmax_player()
    # ttt.play_game(random_player, random_player)

    random_player(ttt, my_state)

    ttt.play_game(minmax_player, random_player)
    # ttt.play_game(alpha_beta_player, minmax_player)


if __name__ == "__main__":
    main()
