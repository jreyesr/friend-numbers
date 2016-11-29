from enum import Enum


class Board:
    SIZE = 10

    def __init__(self):
        """
        Initialize a blank Board, of size Board.SIZE x Board.SIZE
        """
        self._contents = [[Color.Blank for _ in range(Board.SIZE)] for _ in
                          range(Board.SIZE)]

    def __str__(self):
        """
        Return a string representation of the Board
        """
        rows = []
        for i in range(Board.SIZE):
            rows.append(
                "|" + " ".join([str(c.value) for c in self.row(i)]) + "|")
        return '\n'.join(rows)

    def random_fill(self):
        """
        Randomly fill the board with colors, except Blank
        """
        from random import choice
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                self.set_item(i, j, choice(
                    [element for element in Color if element != Color.Blank]))

    def fill_with(self, color):
        """
        Fill the board with the designated color
        :param color: The Color to fill the board with
        """
        self._contents = [[color for _ in range(Board.SIZE)] for _ in
                          range(Board.SIZE)]

    def row(self, i):
        """
        Return a list containing row i of the board
        """
        return self._contents[i]

    def column(self, j):
        """
        Return a list containing column j of the board
        """
        return [row[j] for row in self._contents]

    def item(self, i, j):
        """
        Return item at position (i,j) of the board
        """
        return self._contents[i][j]

    def set_row(self, i, new_row):
        """
        Set row i of the board with the values in new_row
        :param i: The index of the row to be replaced
        :param new_row: A list of new values. it is assumed that len(new_values)>=Board.SIZE
        """
        self._contents[i] = new_row

    def set_column(self, j, new_column):
        """
        Set column j of the board with the values in new_row
        :param i: The index of the row to be replaced
        :param new_row: A list of new values. it is assumed that len(new_values)>=Board.SIZE
        """
        for i in range(Board.SIZE):
            self._contents[i][j] = new_column[i]

    def set_item(self, i, j, new_item):
        """
        Set item (i,j) of the board with the color on new_item
        :param i: The row of the item to be replaced
        :param j: The column of the item to be replaced
        :param new_item: The new value to be stored
        """
        self._contents[i][j] = new_item

    def column_compacted(self, j):
        """
        Return a copy of column j, with all Blank items at the top
        :param j: The index of the column to analyze
        """
        not_zeroes = [x for x in self.column(j) if x != Color.Blank]
        zeroes = [Color.Blank for _ in range(Board.SIZE - len(not_zeroes))]
        return zeroes + not_zeroes

    def compact_column(self, j):
        """
        Set column j to be its compacted version
        :param j: The index of the column to modify
        """
        self.set_column(j, self.column_compacted(j))

    def compact_all(self):
        for j in range(Board.SIZE):
            self.compact_column(j)

    def clear_items(self, list_to_clear):
        """
        Set every item in list_to_clear to be Blank
        :param list_to_clear: A list of items to erase
        """
        for i, j in list_to_clear:
            self.set_item(i, j, Color.Blank)


class Color(Enum):
    A = 1
    B = 2
    C = 3
    D = 4
    Blank = 0
