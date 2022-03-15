from board import Property, Jail

class Player:
    def __init__(self, board, bot=False):
        self.board = board
        self.bot = bot
        self.piece = ""
        self.funds = 1500
        self.net_worth = 0
        self.position = 0
        self.name = "Bot" if bot else "Human"
        self.jailed = False

    def jail(self):
        for index, tile in self.board.tiles:
            if not isinstance(tile, Jail):
                continue
            self.position = index
            break
        self.jailed = True

    def properties(self):
        return [prop for prop in self.board.tiles if isinstance(prop, Property) and prop.owner is self]
    
    def assets_worth(self):
        worth = 0
        
        # properties
        #     its houses
        
        return worth

    def current_tile(self):
        return self.board.get(self.position)

    def react_landing(self):
        current_tile = self.current_tile()
        
        if not hasattr(current_tile, "on_landed"):
            return
        
        getattr(current_tile, "on_landed")(self)

    def color_groups(self):
        return

    # just learned that python has a property() function that
    # avoid formal get-setters

    def has_property(self, this_property):
        return this_property.owner is self

    
    def has_group(self, group):
        if group not in self.board.groups:
            return

        # there has to be a built-in function to wrap around this one
        return all([self.has_property(prop) for prop in self.board.groups[group]])

    def __str__(self):
        return f"{self.piece} {self.name}"

    def move(self, steps):
        new = self.position + steps
        self.position = self.board.mod(new)
        return new > self.position # passed go?

    def gain(self, funds):
        self.funds += funds
        self.net_worth += abs(funds)
