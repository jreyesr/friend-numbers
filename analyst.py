from board import Board, Color


class BoardAnalyst:
    def __init__(self, board_to_watch):
        """
        Create an Analyst that watches and reports status of a Board
        :param board_to_watch: A Board that will be binded to the Analyst
        """
        self.board = board_to_watch

    def neighs(self, i, j):
        """
        Return all neighbours of place (i,j): two if in corner, three if in side, four if inside board
        :param i: The row of the place to analyze
        :param j: The column of the place to analyze
        :return: A list containing tuples of ints, so that 2<=len(X)<=4
        """
        vert_neighs = []
        if i > 0:
            vert_neighs.append((i - 1, j))
        if i < Board.SIZE - 1:
            vert_neighs.append((i + 1, j))

        horz_neighs = []
        if j > 0:
            horz_neighs.append((i, j - 1))
        if j < Board.SIZE - 1:
            horz_neighs.append((i, j + 1))

        return vert_neighs + horz_neighs

    def friend_neighs(self, i, j):
        """
        Return all neighbours of (i,j) that have THE SAME COLOR as it, and nothing if (i,j) is blank or has no friends
        :param i: The row of the place to analyze
        :param j: The column of the place to analyze
        :return: A list containing tuples of ints that are to a side of (i,j) and have the same color as it
        """
        if self.board.item(i, j) == Color.Blank:
            return []
        return [x for x in self.neighs(i, j) if
                self.board.item(x[0], x[1]) == self.board.item(i, j)]

    def has_friends(self, i, j):
        """
        Return True if (i,j) has any neighbour with the same color as it and (i,j) is not blank, False otherwise
        """
        if self.board.item(i, j) == Color.Blank:
            return False
        return len(self.friend_neighs(i, j)) != 0

    def all_friends(self, i, j):
        """
        Return (i,j) plus every item that has the same color as (i,j) and is DIRECTLY connected to it
        'A is directly connected to B' means 'A is connected to B via items of the same color as A *and* B'
        :param i: The row of the place to analyze
        :param j: The column of the place to analyze
        :return: A list of items of the same color and neighbours of each other
        """
        return self._analyze([], [(i, j)])

    def _analyze(self, already_seen, to_check):
        """
        Find all non-seen friend neighbours of everyone in to_check
        :param already_seen: A list containing positions to be ignored
        :param to_check: A list containing the items to be checked for friend neighbours
        :return: already_seen, plus to_check, plus the friend neighbors of everyone in to_check, ad so on...
        """
        if not to_check: return already_seen
        updated_seen = already_seen + to_check
        new_to_check = []
        for i, j in to_check:
            for candidate in self.friend_neighs(i, j):
                if candidate not in updated_seen and candidate not in new_to_check:
                    new_to_check.append(candidate)
        return self._analyze(updated_seen, new_to_check)

    def score(self, squares_list):
        """
        Return the score associated with a specific list of squares.
        Assumes squares_list has at least two elements and that they are all friends
        :param squares_list: The list of positions to remove
        :return: An int representing the score to be given for squares_list
        """
        x = len(squares_list)
        if x == 2:
            return 2
        elif x == 3:
            return 4
        elif x == 4:
            return 8
        elif x == 5:
            return 14
        elif x == 6:
            return 22
        elif x == 7:
            return 32
        elif x == 8:
            return 44
        elif x == 58:
            return 58
        else:
            return 74

    def any_friends(self):
        """
        Return True if any item in the board has friends, False otherwise
        """
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                if self.has_friends(i, j):
                    return True
        return False
