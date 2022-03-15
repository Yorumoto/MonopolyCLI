import globals
from globals import CardSpaceLandType, Groups
from globals import clr as clrtxt
from globals import format_money as fmtcash

import time

class IndividualSite:
    def __init__(self, name="", cost=1000):
        self.name = name
        self.cost = cost
        self.owner = None

    def __str__(self):
        return f'{self.name} | {fmtcash(self.cost)}'
    
class Tax(IndividualSite):
    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return f'{self.name} | {fmtcash(self.cost)}'
    
    def on_landed(self):
        pass

class Jail:
    name = "👮 Go to Jail"

    def on_landed(self, player):
        player.jail()

    def __str__(self):
        return self.name

class NonePlace:
    def __init__(self, name):
        self.name = name

    __str__ = lambda self: self.name

class FreeParking:
    name = "Free Parking"

EMOJI_CARDSPACE = {
    CardSpaceLandType.CommunityChest : '📦',
    CardSpaceLandType.Chance : '❔',
}

STR_CARDSPACE = {
    CardSpaceLandType.CommunityChest : 'Community Chest',
    CardSpaceLandType.Chance : 'Chance',
}

class CardSpace:
    def __init__(self, card_type):
        self.card_type = card_type

    def on_landed(self, player):
        pass

    def __str__(self):
        return f'{EMOJI_CARDSPACE[self.card_type]} {STR_CARDSPACE[self.card_type]}'

class Go:
    color = '\033[42'
    salary = 200

    def __str__(self):
        return clrtxt(f"GO! {fmtcash(self.salary)} Salary", self.color)

class Property:
    def __init__(self, name, group, cost=100, mortgage_gain=1000, house_cost=50, rent=50, *house_rent):
        self.name = name
        self.group = group
        self.cost = cost
        self.house_cost = house_cost
        self.rent = [rent, *house_rent]
        self.houses = 0 # 5 = hotel; 1-4 it's obvious
        self.mortgaged = False
        self.owner = None

    def occupied(self):
        return self.owner is not None

    def on_landed(self, player):
        if not self.occupied:
            globals.yes_no(f'Would you like to buy {self}? You have {fmtcash(player.funds, below=self.cost, colorful=True)}')  
            return

    def __str__(self):
        s = f'{self.group} {self.name} | {fmtcash(self.cost)}'
        return s

class Utility(IndividualSite):
    cost = 150
    
    def __init__(self, name):
        super().__init__(name, self.cost)

    def on_landed(self, player):
        pass

    def __str__(self):
        return f'🔧 {super().__str__()}'

class Railroad(IndividualSite):
    cost = 200

    def __init__(self, name):
        super().__init__(name, self.cost)

    def on_landed(self, player):
        pass

    def __str__(self):
        return f'🚆 {super().__str__()}'


_pint = lambda p: int(p)
_get_prop_group = lambda p: getattr(Groups, p)
_util_rail = {
    1: _pint
}

class Board:
    parse_props = {
        'prop': Property,
        'rail': Railroad,
        'util': Utility,
        'card': CardSpace,
        'jail': Jail,
        'go': Go,
        'tax': Tax,
        'park': FreeParking,
        'noneplace':NonePlace
    }

    parse_args = {
        'card': {
            0: lambda p: getattr(CardSpaceLandType, p)
        },
        'tax' : {1: _pint},
        'util': _util_rail,
        'prop': {i: (_get_prop_group if i == 1 else _pint) for i in range(1, 11)}
    }

    def __init__(self, game):
        self.tiles = []
        self.game = game
        self.groups = {}

    def mod(self, position):
        return position % len(self.tiles)

    def get(self, position):
        return self.tiles[self.mod(position)]
    
    def str(self, start):
        player_positions = {}

        for player in self.game.players:
            if not player.position in player_positions:
                player_positions[player.position] = []

            if not player in player_positions[player.position]:
                player_positions[player.position].append(player)

        l = f"{'─'*50}"
        s = ''

        for position in range(start, start + self.view):
            vacant = 16
            player_dsp = ''

            if position in player_positions:
                player_dsp = ''.join([x.piece for x in player_positions[position]])
                vacant -= len(player_positions[position]) * 2

            tile = self.get(position)
            ns = f"{player_dsp}{' ' * (vacant)}{tile}"
            s += f"{ns}\n"

        return l+'\n'+s+l
    
    def load(self, filename):
        # print(self.parse_args['prop'])

        with open(filename, 'r') as f:
            for line in [x.strip() for x in f.readlines()]:
                if line.startswith('"'):
                    self.view = int(line.split('"')[1])
                    continue

                syntax = [x.strip() for x in line.split(',')]
                
                if line.startswith('#') or not syntax or syntax[0] not in self.parse_props:
                    continue
                
                header = syntax[0]
                class_header = self.parse_props[header]

                if header in self.parse_args:
                    edit_args = self.parse_args[header]

                    for i, arg in enumerate(syntax[1:-1]):
                        if i not in edit_args:
                            continue
                        syntax[i+1] = edit_args[i](arg)
                               
                n = class_header(*syntax[1:-1])
                
                if isinstance(n, Property):
                    if not n.group in self.groups:
                        self.groups[n.group] = []

                    if not n in self.groups[n.group]:
                        self.groups[n.group].append(n)

                self.tiles.append(n)
        
         # for x in self.groups[Groups.Magneta]: print(x)
        
