from enum import Enum

class CardSpaceLandType(Enum):
    CommunityChest = 1
    Chance = 2

# i feel like i should omit the __init__

def clr(text, color="0"):
    return f"\033[{color}m{text}\033[0m"

class ColorGroup:
    def __init__(self, symbol, color='0'):
        self.color = str(color)
        self.symbol = symbol    
    
    def __str__(self):
        return clr(self.symbol, self.color)


class Groups:
    Brown = ColorGroup("BR", '41')
    Cyan = ColorGroup("CY", '106;90')
    Magneta = ColorGroup("MG", '45')
    Orange = ColorGroup("OR", '43')
    Red = ColorGroup("RD", '101')
    Yellow = ColorGroup("YW", '103;90')
    Green = ColorGroup("GR", '42')
    Blue = ColorGroup("BL", '44')

def safe_number_input(text):
    while True:
        try:
            return int(input(text).strip())
        except ValueError:
            pass

# imagine using .format
def format_money(amount, colorful=False, below=0):
    return clr('${:.2f}M'.format(amount / 100), ('31' if amount > below else '41') if colorful else '')

yes_no_prompts = {'y':True,'n':False}

# upgrade y/n func as an upgrade separate function (def letter_chose), yes_no func as a template for letter_chose
# if needed

def yes_no(prompt="Yes/No Prompt"):
    while True:
        inp = input(prompt + " (Y/n)").lower().strip()
        if inp in yes_no_prompts:
            continue
        return yes_no_prompts[inp]


def pick_items(items, prompt="Picked item of choice"):
    listed = False
    ind = None
    
    if isinstance(items, list):
        items = {str(index + 1): item for index, item in enumerate([([x] if not isinstance(x, list) else x) for x in items]
)}
    elif items is None:
        items = {}
    
    items = {item: value for item, value in sorted(items.items())}

    while True:
        if not listed:
            for key, item in items.items():
                print(f'{key}: {item[1] if len(item) > 1 else item[0]}')
            listed = True

        ind = input(f"{prompt}: ").strip().lower()
        
        if ind == 'list':
            listed = False
        else:
            try:
                return items[ind][0]   
            except Exception: 
                print("Sorry, please try again. (Use 'list' if you want to see a list of items)")

# GroupItems = [Groups.Brown, Groups.Cyan, Groups.Magneta, Groups.Orange, Groups.Red, Groups.Yellow, Groups.Green, Groups.Blue]

game = None

def save_game():
    if game is not None:
        try:
            print('Saving game...')
        except Exception:
            print(clr("Failure to save game, use --debug for more information on this error.", '41'))
            
            if debug_flag:
                print(traceback.format_exc())
        finally:
            print(clr('Game saved!', '42'))
    else:
        pass

PIECES_FILENAME = ".pieces"

pieces = []

with open(PIECES_FILENAME, 'r') as f:
    pieces = [x for x in f.read().strip() if x.strip()]
