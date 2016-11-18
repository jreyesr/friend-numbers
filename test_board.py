from analyst import BoardAnalyst
from board import Board, Color

board = Board()
analyzer = BoardAnalyst(board)

board.fill_with(Color.B)

board.set_item(1, 0, Color.A)
board.set_item(2, 0, Color.A)
board.set_item(3, 0, Color.A)
board.set_item(4, 0, Color.A)
board.set_item(3, 1, Color.A)
board.set_item(3, 2, Color.A)
board.set_item(3, 3, Color.A)
board.set_item(3, 4, Color.A)
board.set_item(4, 2, Color.A)

print(board)
print()

board.clear_items(analyzer.all_friends(4, 4))

print(board)
print()

board.compact_all()

print(board)
