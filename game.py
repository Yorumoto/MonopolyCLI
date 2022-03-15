import globals
import board
import time
import random
from player import Player

BOARD_STRUCTURE_FILENAME = ".brdtmp"

class GameClass:
    def __init__(self, player_amount=4):
        self.board = board.Board(self)
        self.board.load(BOARD_STRUCTURE_FILENAME)
        self.turn_index = 0
        self.is_new = False
        self.doubles = 0
        self.doubles_count = 0
        # self.players = [Player(self.board, bot=i>0) for i in range(4)]
        
        # test two variables
        self.players = []
        ids = {True:0, False:0}

        for i in range(player_amount):
            bot = i>0
            nwp = Player(self.board, bot=bot)
            nwp.name = f"{'Robot' if bot else 'Human'} #{ids[bot]+1}"
            ids[bot] += 1
            self.players.append(nwp)

        # whoever gets to roll the highest score gets to go first!
        random.shuffle(self.players)

current_game : GameClass

def player_choice_items(self, view_self=True):
    choices = {}
    
    off = 0

    for i, player in enumerate(current_game.players):
        if player is self:
            off = 1
            continue

        choices[str((i-off)+1)] = [player, str(player)]

    if view_self and self is not None:
        choices['self'] = [self, str(self)]
    
    choices['exit'] = [None, 'Exit selection']

    return choices

    # don't do longass comprehensions
    # return {('self' if player is self else str(i+1)): [player, str(player)] for i, player in enumerate(current_game.players) if (player is self and view_self) or view_self}

def new_game():
    global current_game
    globals.game = GameClass()
    current_game = globals.game

def roll():
    print(globals.clr("Rolling...", "6"))
    time.sleep(random.randint(35, 200) / 100)

    a = [random.randint(1, 6), random.randint(1, 6)]
    print('Rolled a', *a, f"= {sum(a)}")
    return a

def trade():
    pass

def view_side(player):
    print(current_game.board.str((player.position // (current_game.board.view)) * (current_game.board.view - 1)))

def miniprofile(_):
    player = globals.pick_items(player_choice_items(_))

    if player is None:
        return

    # print(f"{globals.clr(f'{player}:'}\nFunds: {globals.format_money(player.funds)}\nNet Worth: {globals.format_money(player.net_worth)}\nProperties Owned:{len(player.properties())}")
    print(
f'''
{'─'*50}
{globals.clr(f'{player}', '107;30')}
Funds: {globals.format_money(player.funds)}
Net Worth: {globals.format_money(player.net_worth)}
Properties Owned: {len(player.properties())}
Assets Worth: {player.assets_worth()}
{'─'*50}
'''
    )

def mroll(player):
    dice = roll()
    passed_go = player.move(sum(dice))
    time.sleep(0.5)
    view_side(player)

    if passed_go:
        salary = current_game.board.get(0).salary
        player.gain(salary)
        print(globals.clr(f'Passed GO! Collected {globals.format_money(salary)}', '42'))

    print(f"Landed at {current_game.board.get(player.position)}")
    time.sleep(1)
    player.react_landing()
    return 1

def setup_game():
    # global roll # wtf??????????????????/


    pieces = globals.pieces[:]
    # print(id(pieces), id(globals.pieces))
    
    # the highest phase, idk
    
    if not globals.debug_flag:
        order = {}

        for player in current_game.players:
            s = f"{player.name}, it's your turn to roll on who gets to be the first."
            
            while True:
                if not player.bot:
                    input(f"{s} (Press any key to roll)")
                else:
                    print(f"{player.name}'s turn.")

                d = sum(roll())

                if d not in order:
                    order[d] = player
                    break
                else:
                    s = "Roll again, {order[d]} already claimed the score."

        order = {name:value for [name, value] in sorted(order.items(), key=lambda item: item[0])}
        current_game.players = list(order.values())
       
        loop_items = order.items()
        
        print('─' * 50)
        for i, [rolled, player] in enumerate(loop_items):
            print(f'{i+1}. {player} | Rolled {rolled}')
        print('─' * 50)
        
        time.sleep(1)

    # pick ur lil pieces
    
    for player in current_game.players:
        player.piece = globals.pick_items(pieces, prompt="Choose your piece") if not player.bot else random.choice(pieces)
        pieces.pop(pieces.index(player.piece))
        
        #if player.bot: 
        print(f'{player.name} has picked {player.piece}')
        
        if not globals.debug_flag:
            time.sleep(random.randint(50, 165) / 100)

    # now let's go dsp whose turn is it!

user_action_prompt = [
        [mroll, "Roll dice"], 
        [view_side, "View where you are"], [trade, "Trade"],
        # nop not doin' it
        # [lambda self: _mnipr(self), "View your own profile in short"],
        [miniprofile, "View someone's profile in a short summary"]
]

def loop():
    # print(current_game.players)
    player = current_game.players[current_game.turn_index]
    print(f"{player.name}, it's your turn!" if not player.bot else f"{player.name}'s turn")
    view_side(player)
    
    if not player.bot:
        while globals.pick_items(user_action_prompt)(player) != 1:
            pass
        input('Press any key to end your turn.')
    else:
        # ai
        pass

    current_game.turn_index = (current_game.turn_index + 1) % len(current_game.players)
    return 0

def program():
    global current_game
    
    # fuyck you lspconfig
    if not current_game.is_new:
        setup_game()
        time.sleep(1)

    while loop() != 1:
        pass
