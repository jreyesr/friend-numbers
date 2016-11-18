from string import ascii_uppercase
from tkinter import *

from board import Color


class GuiDisplayer():
    _score_label = None
    _score = 0

    def __init__(self, board, analyst):
        self._board = board
        self._analyst = analyst

    def display(self):
        def operate_on_button(i, j):
            self._score += self._analyst.score(self._analyst.all_friends(i, j))
            self._score_label.configure(text=str(len(self._analyst.all_friends(i, j))))

        root = Tk()
        Grid.rowconfigure(root, 0, weight=1)

        upper_frame = Frame(root, borderwidth=10)
        upper_frame.grid(row=0, column=0, sticky=N + S + E + W)

        buttons = [[0 for _ in range(11)] for _ in range(11)]
        for row_index in range(10):
            Grid.rowconfigure(upper_frame, row_index, weight=1)
            for col_index in range(10):
                Grid.columnconfigure(upper_frame, col_index + 1, weight=1)
                btn = Button(upper_frame, command=lambda x=row_index, y=col_index: operate_on_button(x, y))
                btn.configure(bg=GuiDisplayer.get_color(self, row_index, col_index))
                buttons[row_index][col_index] = btn
                btn.grid(row=row_index, column=col_index + 1, sticky=N + S + E + W, padx=2, pady=2)

        # Set labels
        for i in range(10):
            Label(upper_frame, text=ascii_uppercase[i]).grid(row=i, column=0, sticky=N + S + E + W)
        for j in range(10):
            Label(upper_frame, text=str(j + 1)).grid(row=10, column=j + 1, sticky=N + S + E + W)

        # Set additional info
        lower_frame = Frame(root)
        lower_frame.grid(row=1, column=0, sticky=N + S + E + W)
        Grid.rowconfigure(lower_frame, 0, weight=1)
        Grid.columnconfigure(lower_frame, 0, weight=1)
        Grid.columnconfigure(lower_frame, 1, weight=1)

        # Score label
        lbl = Label(lower_frame, text="Score")
        self._score_label = lbl
        lbl.grid(row=0, column=0, sticky=N + S + E + W, padx=5, pady=5)
        # Exit game button
        Button(lower_frame, text="Exit", command=lambda: root.destroy()).grid(row=0, column=1, sticky=N + S + E + W,
                                                                              padx=20, pady=5)

        root.mainloop()

    def get_color(self, i, j):
        if self._board.item(i, j) == Color.A:
            return 'red'
        elif self._board.item(i, j) == Color.B:
            return 'green'
        elif self._board.item(i, j) == Color.C:
            return 'blue'
        elif self._board.item(i, j) == Color.D:
            return 'yellow'
        else:
            return 'blank'
