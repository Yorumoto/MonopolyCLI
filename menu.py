import globals
from globals import pick_items
import os
import game

def quit():
    raise KeyboardInterrupt

def new_game():
    game.new_game()
    game.program()

def continue_game():
    err = None

    if not os.path.isfile('.curgame'):
        err = "No game to continue..."

    if err is None:
        try:
            int('d')
        except Exception:
            err = "Continued game file is corrupted"

    if err:
        print(globals.clr(err, '41'))
        return 1
    else:
        game.program()

def game_selection():
    while pick_items([
        [new_game, 'New game'],
        [continue_game, 'Continue game'],
        [lambda: 0, 'Back to main menu']
    ])() == 1:
        pass

def program():
    print('M O N O P O L Y  C L I')
    pick_items([[game_selection, 'Play game'], [quit, 'Quit (or Ctrl+C)']])()
