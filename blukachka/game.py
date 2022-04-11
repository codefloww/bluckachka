class Room:
    def __init__(self, name) -> None:
        self.name = name
        self.north = None
        self.east = None
        self.south = None
        self.west = None
        self.item = None
        self.character = None

    def set_description(self,description) -> None:
        self.description = description

    def link_room(self, room, direction) -> None:
        if direction == 'north' and self.north is None:
            self.north = room
        elif direction == 'east' and self.east is None:
            self.east = room
        elif direction == 'south' and self.south is None:
            self.south = room
        elif direction == 'west' and self.west is None:
            self.west = room
        else:
            print("Can't link rooms!")

    def set_character(self,character) -> None:
        self.character = character

    def set_item(self, item) -> None:
        self.item = item

    def get_details(self) -> None:
        print(f"""{self.name}
------------------------
{self.description}""")    
        if self.south:
            print(f'The {self.south.name} is south')
        if self.north:
            print(f'The {self.north.name} is north')
        if self.east:
            print(f'The {self.east.name} is east')
        if self.west:
            print(f'The {self.west.name} is west')

    def get_item(self) -> object:
        return self.item

    def get_character(self) -> object:
        return self.character

    def move(self,direction) -> object:
        directions = {'north': self.north, 'east': self.east, 'south': self.south, 'west':self.west}
        return directions[direction]

class Creature:
    def __init__(self, name, description) -> None:
        self.name = name
        self.description = description

    def set_conversation(self,conversation) -> None:
        self.replique = conversation

    def describe(self) -> None:
        print(f'{self.name} is here!')
        print(self.description)

    def talk(self) -> None:
        print(f'[{self.name} says]: {self.replique})')

class Enemy(Creature):
    defeated = 0
    def set_weakness(self, weakness) -> None:
        self.weakness = weakness

    def fight(self, weapon) -> None:
        if self.weakness == weapon:
            print(f'You fend {self.name} off with the {weapon}')
            Enemy.defeated +=1
            return True
        else:
            print(f'{self.name} crushes you, puny adventurer!')
            return False
    def get_defeated(self) -> int:
        return Enemy.defeated

class Friend(Creature):
    pass

class Item:
    def __init__(self, name) -> None:
        self.name = name
    def set_description(self, description) -> None:
        self.description = description
    def describe(self):
        print(f'The [{self.name}] is here - {self.description}')
    def get_name(self) -> str:
        return self.name
   
