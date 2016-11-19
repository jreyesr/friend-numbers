# friend-numbers

A game about matching numbers. Choose coordinates to clear said location and all neighbours of the same color.

Board at board.py
---
Stores the data contained in a single game board. Most important methods are:
#### random_fill
Should be used only once in every Board, right after creation. Populates the Board randomly with every color in Color, except Blank.
#### row(i), set_row(i, new_row)
Get and set row at position i (zero-indexed) respectively.
#### column(j), set_column(j, new_column)
Same, but with columns.
#### item(i, j), set_item(i, j, new_item)
Same, but with single items.
#### column_compacted(j), compact_column(j)
Groups all Blanks in column j at the top, and any other items at the bottom, without changing their order. column_compacted does not alter the actual board data, while compact_column does.
#### compact_all()
Applies compact_column() to every column in the board.

BoardAnalyst at analyst.py
---
Reports data about a Board. Most important methods are:
#### neighs(i, j)
Returns all neighbours of item (i, j): two if (i, j) is a corner, three if it is a side and four otherwise.
#### friend_neighs(i ,j)
Returns all neigbours of (i, j) that have the same color as it. Blank items have no friends, by definition.
#### all_friends(i, j)
Core function of BoardAnalyst. Returns (i, j), plus all friend neigbours of (i, j), plus all friend neighbours of said neighbours, to the infinity and beyond...
#### score(item_list)
Returns the score associated with a list of items. Score varies based on the length of the list. Assumes all items in the list are friends.
#### any_friends()
Returns True if there is any item in the board with friends (a.k.a. if the game can continue)

ConsoleDisplayer at console_displayer.py
---
Runs the game in console mode. Execution flow is as follows:
1. show_main_menu is called. It shows three options:
    1. New game: calls start_new_game
        1. Asks the user for his name
        2. Creates a new Board, randomly filled, and an Analyst for that board. Then calls play_game.  
            While there is something to be played:
            * Print the board, ask the user for input. Only two inputs are valid: the exit string or a coordinate with friends and that is not Blank. Any other input displays an error message and repeats.  
            The exit string terminates the loop.
            * if the player entered coordinates, the score is increased and the board is updated. the new score is shown to the user.
            * The loop is repeated.
        3. When play_game returns the score of the game, calls print_game_over, which prints the player name and score.
        4. Control is returned to the main menu
    2. About: calls print_about and returns to main menu
    3. Exit: Prints personalized message to player (only if name is set). Then exits.

GUIDisplayer at gui_displayer.py
---
Runs the game in graphical mode. Execution flow is as follows:
1. MainMenuWindow is created, with three buttons:
    1. New Game: Creates NameWindow, which asks the user for his name. NameWindow then creates a Board, an Analyst and a GameWindow, which has two kinds of buttons:
        * Coordinate buttons: These buttons are colored. Clicking on them updates the score, the board and the buttons, if the button corresponds to an item with friends; and does nothing otherwise.
        * End game button: Finishes the game and creates a GameOverWindow, which shows the player name and the achieved score.
            * GameOverWindow has a single button, which creates a new MainMenuWindow, resetting the execution flow to point 1.
    2. About: Creates an AboutWindow, which has a single button that creates a new MainMenuWindow, resetting the execution flow to point 1.
    3. Exit: Only if name is set, creates a GoodByeWindow, which shows a personalized message to last player. Then exits.
