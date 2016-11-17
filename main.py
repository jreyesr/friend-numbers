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

from board import Board

b = Board()
print(b)
