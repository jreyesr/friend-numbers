from enum import Enum


class Board:
    SIZE = 10

    def __init__(self):
        self.fill_with(Color.Blank)

    def __str__(self):
        rows = []
        for i in range(Board.SIZE):
            rows.append("|" + " ".join([str(c.value) for c in self.row(i)]) + "|")
        return '\n'.join(rows)

    def random_fill(self):
        from random import choice
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                self.set_item(i, j, choice([element for element in Color if element != Color.Blank]))

    def fill_with(self, color):
        self._contents = [[color for _ in range(Board.SIZE)] for _ in range(Board.SIZE)]

    def row(self, i):
        return self._contents[i]

    def column(self, j):
        return [row[j] for row in self._contents]

    def item(self, i, j):
        return self._contents[i][j]

    def set_row(self, i, new_row):
        self._contents[i] = new_row

    def set_column(self, j, new_column):
        for i in range(Board.SIZE):
            self._contents[i][j] = new_column[i]

    def set_item(self, i, j, new_item):
        self._contents[i][j] = new_item

    def column_compacted(self, j):
        not_zeroes = [x for x in self.column(j) if x != Color.Blank]
        zeroes = [Color.Blank for _ in range(Board.SIZE - len(not_zeroes))]
        return zeroes + not_zeroes

    def compact_column(self, j):
        self.set_column(j, self.column_compacted(j))

    def compact_all(self):
        for j in range(Board.SIZE):
            self.compact_column(j)

    def clear_items(self, list_to_clear):
        for i, j in list_to_clear:
            self.set_item(i, j, Color.Blank)


class Color(Enum):
    A = 1
    B = 2
    C = 3
    D = 4
    Blank = 0
