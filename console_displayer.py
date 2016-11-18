from string import ascii_uppercase


class ConsoleDisplayer:
    def __init__(self, board, analyst):
        self._board = board
        self._analyst = analyst

    def display(self):
        for i in range(self._board.SIZE):
            print(ascii_uppercase[i] + "\u2502" + ' '.join([str(x.value) for x in self._board.row(i)]))
        print(" \u2514" + "\u2500" * (self._board.SIZE * 2 - 1))
        print("  " + ' '.join(str(x + 1) for x in range(self._board.SIZE)))
