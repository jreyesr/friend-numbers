from string import ascii_uppercase
from tkinter import *

from board import Color


class GuiDisplayer():
    _score_label = None
    _score = 0
    _buttons = None
    current_window = None

    def __init__(self, board, analyst):
        self._board = board
        self._analyst = analyst
        self._buttons = [[0 for _ in range(self._board.SIZE + 1)] for _ in range(self._board.SIZE + 1)]

    def button_clicked(self, i, j):
        if not self._analyst.has_friends(i, j) or self._board.item(i, j) == Color.Blank:
            return
        to_clear = self._analyst.all_friends(i, j)
        self._score += self._analyst.score(to_clear)
        self._board.clear_items(to_clear)
        self._board.compact_all()
        self._score_label.configure(text="Puntos: {}".format(self._score))

        if not self._analyst.any_friends():
            self.end_game()

        self.update()

    @staticmethod
    def open(window):
        GuiDisplayer.current_window = window
        window.mainloop()

    @staticmethod
    def close():
        GuiDisplayer.current_window.destroy()
        GuiDisplayer.current_window = None

    def main_window(self):
        root = Tk()
        Grid.rowconfigure(root, 0, weight=1)

        upper_frame = Frame(root, borderwidth=10)
        upper_frame.grid(row=0, column=0, sticky=N + S + E + W)

        for row_index in range(self._board.SIZE):
            Grid.rowconfigure(upper_frame, row_index, weight=1)
            for col_index in range(self._board.SIZE):
                Grid.columnconfigure(upper_frame, col_index + 1, weight=1)
                btn = Button(upper_frame, command=lambda x=row_index, y=col_index: self.button_clicked(x, y))
                btn.configure(bg=self.get_color(row_index, col_index))
                self._buttons[row_index][col_index] = btn
                btn.grid(row=row_index, column=col_index + 1, sticky=N + S + E + W, padx=2, pady=2)

        # Set labels
        for i in range(self._board.SIZE):
            Label(upper_frame, text=ascii_uppercase[i]).grid(row=i, column=0, sticky=N + S + E + W)
        for j in range(self._board.SIZE):
            Label(upper_frame, text=str(j + 1)).grid(row=self._board.SIZE, column=j + 1, sticky=N + S + E + W)

        # Set additional info (score, exit button)
        lower_frame = Frame(root)
        lower_frame.grid(row=1, column=0, sticky=N + S + E + W)
        Grid.rowconfigure(lower_frame, 0, weight=1)
        Grid.columnconfigure(lower_frame, 0, weight=1)
        Grid.columnconfigure(lower_frame, 1, weight=1)

        # Score label
        lbl = Label(lower_frame, text="Puntos: 0")
        self._score_label = lbl
        lbl.grid(row=0, column=0, sticky=N + S + E + W, padx=5, pady=5)
        # Exit game button
        Button(lower_frame, text="Exit", command=lambda: self.end_game()).grid(row=0, column=1,
                                                                               sticky=N + S + E + W, padx=20,
                                                                               pady=5)
        return root

    def update(self):
        for i in range(self._board.SIZE):
            for j in range(self._board.SIZE):
                try:
                    self._buttons[i][j].configure(bg=self.get_color(i, j))
                except:
                    pass

    def end_game(self):
        print("Game has ended now. Score: {}".format(self._score))
        self.close()

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
            return 'gray'
