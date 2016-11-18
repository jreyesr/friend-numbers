from board import Board, Color


class BoardAnalyst:
    def __init__(self, board_to_watch):
        self.board = board_to_watch

    def neighs(self, i, j):
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
        if self.board.item(i, j) == Color.Blank:
            return []
        return [x for x in self.neighs(i, j) if self.board.item(x[0], x[1]) == self.board.item(i, j)]

    def has_friends(self, i, j):
        return len(self.friend_neighs(i, j)) != 0

    def all_friends(self, i, j):
        return self._analyze([], [(i, j)])

    def _analyze(self, already_seen, to_check):
        if not to_check: return already_seen
        updated_seen = already_seen + to_check
        new_to_check = []
        for i, j in to_check:
            for candidate in self.friend_neighs(i, j):
                if candidate not in updated_seen and candidate not in new_to_check:
                    new_to_check.append(candidate)
        return self._analyze(updated_seen, new_to_check)

    def score(self, squares_list):
        # TODO Put intelligent info here!!!
        return 10

    def any_friends(self):
        for i in range(Board.SIZE):
            for j in range(Board.SIZE):
                if self.has_friends(i, j):
                    return True
        return False
