from board import Board, Color

board = Board()
board.set_item(1, 0, Color.Blank)
board.set_item(2, 0, Color.Blank)
board.set_item(3, 2, Color.Blank)
board.set_item(4, 2, Color.Blank)
print(board)
print()
board.compact_all()
print(board)
