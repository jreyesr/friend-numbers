# graph = {'A': [], 'B': [], 'C': [], 'D': [], 'E': ['F'], 'F': ['B', 'E', 'G', 'J'], 'G': ['F', 'K'], 'H': [], 'I': [],
#          'J': ['F', 'K', 'N'], 'K': ['G', 'J','O'], 'L': [], 'M': [], 'N': ['J', 'O'], 'O': ['K', 'N', 'P'],
#          'P': ['O']}
#
#
# def find_all_friends(x):
#     global already_seen
#     already_seen = already_seen if already_seen != [] else [x]
#     new_neighs = [friend for friend in graph[x] if friend not in already_seen]
#     already_seen += new_neighs
#     for neigh in new_neighs:
#         find_all_friends(neigh)
#
#
# already_seen = []
# find_all_friends('E')
# print(already_seen)

from analyst import BoardAnalyst
from board import Board
from console_displayer import ConsoleDisplayer
from gui_displayer import GuiDisplayer

b = Board()
a = BoardAnalyst(b)
d = ConsoleDisplayer(b, a)
g = GuiDisplayer(b, a)

b.random_fill()
d.display()
g.display()
