from string import ascii_uppercase

from analyst import BoardAnalyst
from better_input import choice_input, simple_input
from board import Board


def show_main_menu():
    user_wants_to_exit = False
    last_player = None
    while not user_wants_to_exit:
        user_action = choice_input("Ingrese una opción: ", ["Nuevo juego", "Acerca de", "Salir"],
                                   error_message="No es una opción válida")
        if user_action == 0:
            last_player = start_new_game()
        elif user_action == 1:
            print_about()
        elif user_action == 2:
            user_wants_to_exit = True
    # Print goodbye message (and name?)
    if last_player is not None:
        print("Hasta luego, {}".format(last_player))


def print_about():
    print("\nAbout the game\nDesigned for ESPOL (...)")
    import datetime
    print(datetime.date.today().strftime("%A, %d/%m/%Y"))
    print()


def start_new_game():
    print()
    name = ask_name()

    board = Board()
    board.random_fill()
    analyst = BoardAnalyst(board)

    score = play_game(board, analyst)

    print_game_over(name, score)
    print()
    return name if name != "Sin nombre" else None


def ask_name():
    player_name = simple_input("Ingrese su nombre: ")
    return player_name if len(player_name) > 0 else "Sin nombre"


def play_game(board: Board, analyst: BoardAnalyst):
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
    if user_input.upper() == 'S':
        return True
    try:
        i, j = process_input(user_input)
        return analyst.has_friends(i, j)
    except (IndexError, ValueError):
        return False


def process_input(user_input: str):
    if user_input.upper() == 'S':
        return None
    i = ascii_uppercase.index(user_input[0].upper())
    j = int(user_input[1:]) - 1
    return i, j


def print_game_over(name: str, score: int):
    print("Jugador: {}\nPuntaje: {}".format(name, score))


def print_board(board):
    for i in range(board.SIZE):
        print(ascii_uppercase[i] + "\u2502" + ' '.join([str(x.value) for x in board.row(i)]))
    # Horizontal separator
    print(" \u2514" + "\u2500" * (board.SIZE * 2))
    # Bottom row of numbers
    print("  " + ' '.join(str(x + 1) for x in range(board.SIZE)))
