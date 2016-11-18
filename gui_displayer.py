from string import ascii_uppercase
from tkinter import *

from analyst import BoardAnalyst
from board import Board, Color


class MainMenuWindow:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("+100+100")
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.rowconfigure(self.root, 0, weight=1)

        frame = Frame(self.root, borderwidth=10)
        frame.grid(row=0, column=0, sticky=N + S + E + W)

        Button(frame, text="New Game", command=lambda: self.start_new_game()).grid(row=0, column=0, sticky=E + W)
        Button(frame, text="About", command=lambda: self.show_about()).grid(row=1, column=0, sticky=E + W)
        Button(frame, text="Exit", command=lambda: self.exit()).grid(row=2, column=0, sticky=E + W)
        Grid.columnconfigure(frame, 0, weight=1)
        for i in range(3):
            Grid.rowconfigure(frame, i, weight=1)

    def show(self):
        self.root.mainloop()

    def start_new_game(self):
        new_window = NameWindow()
        self.root.destroy()
        new_window.show()

    def show_about(self):
        new_window = AboutWindow()
        self.root.destroy()
        new_window.show()

    def exit(self):
        self.root.destroy()


class NameWindow:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("+100+100")
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.rowconfigure(self.root, 0, weight=1)

        self.text_field = Entry(self.root, justify=CENTER)
        self.text_field.grid(row=0, column=0, sticky=E + W, padx=5, pady=5)
        Button(self.root, text="OK", command=lambda: self.start_game()).grid(row=1, column=0, padx=5, pady=5)

    def show(self):
        self.root.mainloop()

    def start_game(self):
        board = Board()
        board.random_fill()
        analyst = BoardAnalyst(board)

        new_window = GameWindow(self.text_field.get(), board, analyst)
        self.root.destroy()
        new_window.show()


class AboutWindow:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("300x200+100+100")
        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)

        frame = Frame(self.root, borderwidth=10)
        text = Text(frame)
        text.pack(fill=BOTH, expand=1)
        text.insert(END, "About the game\nDesigned for ESPOL (...)")
        frame.grid(row=0, column=0, sticky=N + S + E + W)

        second_frame = Frame(self.root, borderwidth=10)
        second_frame.grid(row=1, column=0)
        Button(second_frame, text="OK", command=lambda: self.close()).grid(row=0, column=0)

    def show(self):
        self.root.mainloop()

    def close(self):
        new_window = MainMenuWindow()
        self.root.destroy()
        new_window.show()


class GameWindow:
    def __init__(self, player_name, board, analyst):
        self.player_name = player_name
        self.score = 0

        self.board = board
        self.analyst = analyst
        self.buttons = [[0 for _ in range(self.board.SIZE + 1)] for _ in range(self.board.SIZE + 1)]

        self.root = Tk()
        self.root.geometry("500x500+100+100")
        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)

        upper_frame = Frame(self.root, borderwidth=10)
        upper_frame.grid(row=0, column=0, sticky=N + S + E + W)

        for row_index in range(self.board.SIZE):
            Grid.rowconfigure(upper_frame, row_index, weight=1)
            for col_index in range(self.board.SIZE):
                Grid.columnconfigure(upper_frame, col_index + 1, weight=1)
                btn = Button(upper_frame, command=lambda x=row_index, y=col_index: self.button_clicked(x, y))
                btn.configure(bg=self.get_color(row_index, col_index))
                self.buttons[row_index][col_index] = btn
                btn.grid(row=row_index, column=col_index + 1, sticky=N + S + E + W, padx=2, pady=2)

        # Set labels
        for i in range(self.board.SIZE):
            Label(upper_frame, text=ascii_uppercase[i]).grid(row=i, column=0, sticky=N + S + E + W)
        for j in range(self.board.SIZE):
            Label(upper_frame, text=str(j + 1)).grid(row=self.board.SIZE, column=j + 1, sticky=N + S + E + W)

        # Set additional info (score, exit button)
        lower_frame = Frame(self.root)
        lower_frame.grid(row=1, column=0, sticky=N + S + E + W)

        Grid.rowconfigure(lower_frame, 0, weight=1)
        Grid.columnconfigure(lower_frame, 0, weight=1)
        Grid.columnconfigure(lower_frame, 1, weight=1)

        # Score label
        lbl = Label(lower_frame, text="Puntos: 0")
        self._score_label = lbl
        lbl.grid(row=0, column=0, sticky=N + S + E + W, padx=5, pady=5)
        # Exit game button
        Button(lower_frame, text="End game", command=lambda: self.end_game()).grid(row=0, column=1,
                                                                                   sticky=N + S + E + W, padx=20,
                                                                                   pady=5)

    def show(self):
        self.root.mainloop()

    def end_game(self):
        new_window = GameOverWindow(self.player_name, self.score)
        self.root.destroy()
        new_window.show()

    def button_clicked(self, i, j):
        if not self.analyst.has_friends(i, j) or self.board.item(i, j) == Color.Blank:
            return
        to_clear = self.analyst.all_friends(i, j)
        self.score += self.analyst.score(to_clear)
        self.board.clear_items(to_clear)
        self.board.compact_all()
        self._score_label.configure(text="Puntos: {}".format(self.score))

        if not self.analyst.any_friends():
            self.end_game()

        self.update()

    def update(self):
        for i in range(self.board.SIZE):
            for j in range(self.board.SIZE):
                try:
                    self.buttons[i][j].configure(bg=self.get_color(i, j))
                except TclError:
                    pass

    def get_color(self, i, j):
        if self.board.item(i, j) == Color.A:
            return 'red'
        elif self.board.item(i, j) == Color.B:
            return 'green'
        elif self.board.item(i, j) == Color.C:
            return 'blue'
        elif self.board.item(i, j) == Color.D:
            return 'yellow'
        else:
            return 'gray'


class GameOverWindow:
    def __init__(self, player_name, score):
        self.player_name = player_name
        self.score = score

        self.root = Tk()
        self.root.geometry("+100+100")
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.rowconfigure(self.root, 0, weight=1)

        frame = Frame(self.root, borderwidth=10)
        frame.grid(row=0, column=0, sticky=N + S + E + W)

        Label(frame, text=player_name).grid(row=0, column=0)
        Label(frame, text="{} puntos".format(score)).grid(row=1, column=0)
        Button(frame, text="OK", command=lambda: self.close()).grid(row=2, column=0)

        Grid.columnconfigure(frame, 0, weight=1)
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.rowconfigure(frame, 1, weight=1)

    def close(self):
        new_window = MainMenuWindow()
        self.root.destroy()
        new_window.show()

    def show(self):
        self.root.mainloop()
