import sys
import traceback
import globals
import menu
import os
import time

if '--free' in sys.argv:
    print(globals.clr("You ain't gonna have that stuff, kid.", "41"))
    raise SystemExit(69)

globals.debug_flag = '--debug' in sys.argv

def program():
    menu.program()
    # game()

def main():
    while True:
        os.system('clear')    
        quit_game = False

        try:
            program()
        except KeyboardInterrupt:
            quit_game = True
        except Exception:
            print(globals.clr(f'A game error occured!\n{traceback.format_exc()}\n{"Will try to save game as it occured in the middle of a match" if globals.game is not None else ""}', '103;30'))
            quit_game = globals.debug_flag

        globals.save_game()

        if quit_game:
            break


if __name__ == '__main__':
    main()
