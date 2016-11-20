from string import ascii_uppercase
from tkinter import *

from analyst import BoardAnalyst
from board import Board, Color


class MainMenuWindow:
    """
    A class that represents a Main Menu. Can branch to a NameWindow, to an AboutWindow or to a GoodByeWindow
    On button 1: Branch to a NameWindow, which will eventually start a new game.
    On button 2: Branch to an AboutWindow, which can only return to a MainMenuWindow.
    On button 3: If any player has given a name, branch to a GoodByeWindow and pass it the player name. Else, kill app.
    """

    def __init__(self, player_name=None):
        """
        Layout of MainMenuWindow is as follows:
        root
         |
         +--frame
              |
              +--Button (Nuevo juego)
              +--Button (Acerca de)
              +--Button (Salir)
        """
        self.name = player_name

        self.root = Tk()
        self.root.focus_force()
        self.root.geometry("+100+100")
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.rowconfigure(self.root, 0, weight=1)

        frame = Frame(self.root, borderwidth=10)
        frame.grid(row=0, column=0, sticky=N + S + E + W)

        Button(frame, text="Nuevo juego", command=lambda: self.start_new_game()).grid(row=0, column=0, sticky=E + W)
        Button(frame, text="Acerca de...", command=lambda: self.show_about()).grid(row=1, column=0, sticky=E + W)
        Button(frame, text="Salir", command=lambda: self.exit()).grid(row=2, column=0, sticky=E + W)
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
        if self.name is not None:
            new_window = GoodByeWindow(self.name)
        self.root.destroy()
        if self.name is not None:
            new_window.show()


class NameWindow:
    """
    A class that represents a Window that asks the user for his/her name. Will only branch to a GameWindow.
    """

    def __init__(self):
        """
        Layout of NameWindow is as follows:
        root
         |
         +--Label
         +--TextField
         +--Button (OK)
        """
        self.root = Tk()
        self.root.geometry("+100+100")
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.rowconfigure(self.root, 0, weight=1)

        Label(self.root, text="Nombre").grid(row=0, column=0, padx=5, pady=5)
        self.text_field = Entry(self.root, justify=CENTER)
        self.text_field.bind("<Return>", self.start_game)
        self.text_field.focus_force()
        self.text_field.grid(row=1, column=0, sticky=E + W, padx=5, pady=5)
        Button(self.root, text="OK", command=lambda: self.start_game(None)).grid(row=2, column=0, padx=5, pady=5)

    def show(self):
        self.root.mainloop()

    def start_game(self, _):
        board = Board()
        board.random_fill()
        analyst = BoardAnalyst(board)

        new_window = GameWindow(self.text_field.get() if len(self.text_field.get()) > 0 else "Sin nombre", board,
                                analyst)
        self.root.destroy()
        new_window.show()


class AboutWindow:
    """
    A class that represent a Window that shows information about the program. Can only branch to a MainMenuWindow
    """

    def __init__(self):
        """
        Layout of NameWindow is as follows:
        root
         |
         +--frame
         |    |
         |    +--Text
         |
         +--second_frame
              |
              +--Button (OK)
        """
        self.root = Tk()
        self.root.geometry("300x200+100+100")
        Grid.rowconfigure(self.root, 0, weight=1)
        Grid.columnconfigure(self.root, 0, weight=1)

        frame = Frame(self.root, borderwidth=10)
        text = Text(frame)
        text.pack(fill=BOTH, expand=1)
        text.insert(END, "About the game\nDesigned for ESPOL (...)\n")

        import datetime
        text.insert(END, datetime.date.today().strftime("%A, %d/%m/%Y"))

        frame.grid(row=0, column=0, sticky=N + S + E + W)

        second_frame = Frame(self.root, borderwidth=10)
        second_frame.grid(row=1, column=0)
        ok_button = Button(second_frame, text="OK", command=lambda: self.close(None))
        ok_button.grid(row=0, column=0)
        ok_button.focus_force()
        ok_button.bind("<Return>", self.close)

    def show(self):
        self.root.mainloop()

    def close(self, _):
        new_window = MainMenuWindow()
        self.root.destroy()
        new_window.show()


class GameWindow:
    """
    A class that represents a Game Window, where most of the processing happens. Can only branch to a GameOverWindow
    """

    def __init__(self, player_name, board, analyst):
        """
        Layout of GameWindow is as follows:
        root
          |
          +--upper_frame
          |      |
          |      +--Labels (in row (Board.SIZE+1) and column 1), total Board.SIZE*2
          |      +--Buttons (in rows 1 to Board.SIZE and columns 2 to Board.SIZE+1, total Board.SIZE^2
          |
          +--lower_frame
                 |
                 +--Label (Puntos...)
                 +--Button (Terminar juego)
        """
        self.player_name = player_name
        self.score = 0

        self.board = board
        self.analyst = analyst
        self.buttons = [[0 for _ in range(self.board.SIZE + 1)] for _ in range(self.board.SIZE + 1)]

        self.root = Tk()
        self.root.focus_force()
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
        Button(lower_frame, text="Terminar juego", command=lambda: self.end_game()).grid(row=0, column=1,
                                                                                         sticky=N + S + E + W, padx=20,
                                                                                         pady=5)

    def show(self):
        self.root.mainloop()

    def end_game(self):
        new_window = GameOverWindow(self.player_name, self.score)
        self.root.destroy()
        new_window.show()

    def button_clicked(self, i, j):
        """
        To be called when a button on the button grid is clicked. If item in said position in the board is not Blank
        and has friends, remove all friends and update score, board and grid accordingly. If there are not any friends
        for any button, end game automatically.
        """
        if not self.analyst.has_friends(i, j) or self.board.item(i, j) == Color.Blank:
            return
        to_clear = self.analyst.all_friends(i, j)
        self.score += self.analyst.score(to_clear)
        self.board.clear_items(to_clear)
        self.board.compact_all()
        self._score_label.configure(text="Puntos: {}".format(self.score))

        if not self.analyst.any_friends():
            self.end_game()

        self.update_button_colors()

    def update_button_colors(self):
        """
        Updates the button grid with the new colors. To be called after changing the Board.
        """
        for i in range(self.board.SIZE):
            for j in range(self.board.SIZE):
                try:
                    self.buttons[i][j].configure(bg=self.get_color(i, j))
                except TclError:
                    pass

    def get_color(self, i, j):
        """
        Return a string representation for the color in position (i, j) in the Board
        :param i: The row of the item
        :param j: The column of the item
        :return: A string to be used in bg
        """
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
    """
    A class representing a 'Game Over' window. Can only branch to a MainMenuWindow.
    """

    def __init__(self, player_name, score):
        """
        Layout of GameOverWindow is as follows:
        root
          |
          +--frame
               |
               +--Label (player name)
               +--Label (score)
               +--Button (OK)
        """
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
        ok_button = Button(frame, text="OK", command=lambda: self.close(None))
        ok_button.grid(row=2, column=0)
        ok_button.focus_force()
        ok_button.bind("<Return>", self.close)

        Grid.columnconfigure(frame, 0, weight=1)
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.rowconfigure(frame, 1, weight=1)

    def close(self, _):
        new_window = MainMenuWindow(self.player_name if self.player_name != "Sin nombre" else None)
        self.root.destroy()
        new_window.show()

    def show(self):
        self.root.mainloop()


class GoodByeWindow:
    """
    A class representing a 'Goodbye' window. Will only branch to nothingness...
    Is only called when MainMenuWindow has a player name stored
    """

    def __init__(self, player_name):
        """
        Layout of GoodByeWindow is as follows:
        root
          |
          +--frame
               |
               +--Label (player name, goodbye message)
               +--Button (OK)
        """
        self.player_name = player_name

        self.root = Tk()
        self.root.geometry("+100+100")
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.rowconfigure(self.root, 0, weight=1)

        frame = Frame(self.root, borderwidth=10)
        frame.grid(row=0, column=0, sticky=N + S + E + W)

        Label(frame, text="Hasta luego, {}".format(player_name)).grid(row=0, column=0, pady=5)
        ok_button = Button(frame, text="OK", command=lambda: self.close(None))
        ok_button.grid(row=1, column=0)
        ok_button.focus_force()
        ok_button.bind("<Return>", self.close)

        Grid.columnconfigure(frame, 0, weight=1)
        Grid.rowconfigure(frame, 0, weight=1)
        Grid.rowconfigure(frame, 1, weight=1)

    def close(self, _):
        self.root.destroy()

    def show(self):
        self.root.mainloop()
