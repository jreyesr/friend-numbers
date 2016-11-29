from string import ascii_uppercase

from terminaltables import AsciiTable

from analyst import BoardAnalyst
from better_input import choice_input, simple_input
from board import Board


def show_main_menu():
    """
    Print the main menu and ask the user for a choice. 1 starts a new game, which eventually returns the player name.
    2 prints info about the program. 3 exits the menu. If a player name has been given, print a good bye to the player.
    """
    user_wants_to_exit = False
    last_player = None
    wanted_difficulty = 10
    while not user_wants_to_exit:
        user_action = choice_input("Ingrese una opción: ",
                                   ["Nuevo juego", "Dificultad", "Acerca de",
                                    "Salir"],
                                   error_message="No es una opción válida")
        if user_action == 0:
            last_player = start_new_game(wanted_difficulty)
        elif user_action == 1:
            wanted_difficulty = ask_difficulty()
        elif user_action == 2:
            print_about()
        elif user_action == 3:
            user_wants_to_exit = True
    if last_player is not None:
        print("Hasta luego, {}".format(last_player))


def print_about():
    """
    Print information about the program and return to caller
    """
    print()
    print("Acerca del juego")
    print(
        "El juego consiste en eliminar los cuadros adyacentes del mismo color de un tablero.")
    print("Los cuadros están colocados de manera aleatoria.")
    print("Cuando se eliminan cuadros, los demás se desplazan hacia abajo.")
    print("Diseñado para Fundamentos de Programación, ESPOL")
    print("Anthony Adachi (KimCordero213)\nJosé Reyes (jreyesr, 0xC0FFEE)")
    import datetime
    print(datetime.date.today().strftime("%A, %d/%m/%Y"))
    print()


def ask_difficulty():
    print()
    x = choice_input("Elija una dificultad: ",
                     ["Fácil (8x8)", "Normal (10x10)", "Difícil (15x15)"],
                     error_message="No es una de las opciones")
    print()
    return [8, 10, 15][x]


def start_new_game(difficulty):
    """
    Ask the user for name, create a Board and an Analyst, enter main game loop (which will return the score) and then
    show a 'Game Over' window with the name and the score
    :return: A string containing the player name, or None if player didn´t originally give a name
    """
    print()
    name = ask_name()

    Board.SIZE = difficulty
    board = Board()
    board.random_fill()
    analyst = BoardAnalyst(board)

    score = play_game(board, analyst)

    print_game_over(name, score)
    print()
    return name if name != "Sin nombre" else None


def ask_name():
    """
    Ask the user for his name and ensure it has any visible characters
    :return: The user's input if it contained anything other than whitespaces, else 'Sin nombre'
    """
    player_name = simple_input("Ingrese su nombre: ")
    return player_name if len(player_name.strip()) > 0 else "Sin nombre"


def play_game(board: Board, analyst: BoardAnalyst):
    """
    Begin a new game on the given Board, using the given Analyst. Return the final score
    :param board: The Board to play on
    :param analyst: The Analyst for the Board
    :return: The score of the game (obtained either by the player ending it or by the game being unable to continue)
    """
    score = 0
    while True:
        print()
        print_board(board)
        if not analyst.any_friends():
            break
        answer = simple_input("Ingrese una coordenada o 'S' para salir: ")
        while not is_valid(answer, analyst):
            print("No es una coordenada válida")
            answer = simple_input("Ingrese una coordenada o 'S' para salir: ")
        answer = process_input(answer)
        if answer is None:
            break
        to_remove = analyst.all_friends(answer[0], answer[1])
        score += analyst.score(to_remove)
        board.clear_items(to_remove)
        board.compact_all()
        print("Puntos: {}".format(score))
    return score


def is_valid(user_input: str, analyst: BoardAnalyst):
    """
    Check the player's input corresponds to an item he can play on
    :param user_input: A string that has to represent a VALID position, WITH friends, and NOT BLANK; or the EXIT string
    :param analyst: The Analyst for the game session
    :return: True if the user's input was sensible, False otherwise
    """
    if user_input.upper() == 'S':
        return True
    try:
        i, j = process_input(user_input)
        return 0 <= i < Board.SIZE and 0 <= j < Board.SIZE and analyst.has_friends(
            i, j)
    except (IndexError, ValueError):
        return False


def process_input(user_input: str):
    """
    Takes a user input and converts it into a position (int, int). Assumes the position is valid (no exception handling)
    :param user_input: The string to be converted to a tuple
    :return: None if the user entered the exit string. Otherwise, a tuple (int, int)
    """
    if user_input.upper() == 'S':
        return None
    i = ascii_uppercase.index(user_input[0].upper())
    j = int(user_input[1:]) - 1
    return i, j


def print_game_over(name: str, score: int):
    """
    Print a short 'Game Over' window showing the player's name and score
    :param name: The name of the player
    :param score: The score the player achieved
    """
    print("Jugador: {}\nPuntaje: {}".format(name, score))


def print_board(board):
    """
    Pretty-print a Board. Use in Terminal/CMD for best results (PyCharm/IPython don't work well with Unicode box chars)
    :param board: The Board to be printed.
    """
    table_data = []
    for i in range(board.SIZE):
        table_data.append(
            [ascii_uppercase[i]] + [str(x.value) for x in board.row(i)])
    table_data.append([""] + [str(x + 1) for x in range(board.SIZE)])
    table = AsciiTable(table_data)
    table.inner_column_border = False
    table.inner_heading_row_border = False
    table.inner_footing_row_border = True
    print(table.table)
