import random


class Street:
    def __init__(self, name: str, description: str = None) -> None:
        self.name = name
        self.nearby_streets = []
        self.creatures = []
        self.items = []
        self.description = description or None

    def set_description(self, description: str) -> None:
        self.description = description

    def link_streets(self, street: object) -> None:
        self.nearby_streets.append(street)
        street.nearby_streets.append(self)

    def set_creature(self, creature: object) -> None:
        self.creatures.append(creature)

    def remove_creature(self, creature: object) -> None:
        self.creatures.remove(creature)

    def set_item(self, item: object) -> None:
        self.items.append(item)

    def remove_item(self, item: object) -> None:
        self.items.remove(item)

    def describe(self) -> None:
        print(
            f"""{self.name}
------------------------
{self.description or "There is no info about street"}"""
        )
        if self.nearby_streets:
            print("Oh, there is some streets nearby:")
            for i, street in enumerate(self.nearby_streets):
                print(f"{i+1} - {street.name}")

    def get_nearby_streets(self) -> list:
        return list(street.name for street in self.nearby_streets)

    def get_items(self) -> list:
        return list(self.items)

    def get_items_by_names(self) -> dict:
        return {item.name: item for item in self.items}

    def get_creatures(self) -> list:
        return list(self.creatures)

    def get_creatures_by_names(self) -> dict:
        return {creature.name: creature for creature in self.creatures}

    def move(self, next_street: str) -> None:
        for street in self.nearby_streets:
            if street.name == next_street:
                return street
        print("Sorry, there's no such street nearby")


class Creature:
    def __init__(self, name: str, description: str = None) -> None:
        self.name = name
        self.repliques = set()
        self.description = description or None

    def set_description(self, description: str) -> None:
        self.description = description

    def add_replique(self, replique: str) -> None:
        self.repliques.add(replique)

    def describe(self) -> None:
        print(f"{self.name} is here!")
        print(self.description)

    def talk(self) -> None:
        if self.repliques:
            replique = random.choice(list(self.repliques))
            print(f"[{self.name} says]: {replique})")

    def is_enemy(self) -> bool:
        return self.aggressive


class Enemy(Creature):
    defeated = 0

    def __init__(self, name: str, description: str = None) -> None:
        super().__init__(name, description)
        self.aggressive = True

    def set_weakness(self, weakness: str) -> None:
        self.weakness = weakness

    def fight(self, weapon: str) -> bool:
        if self.weakness == weapon:
            print(f"You fend {self.name} off with the {weapon}")
            Enemy.defeated += 1
            return True
        else:
            print(f"{self.name} crushes you, puny adventurer!")
            return False

    def get_defeated(self) -> object:
        return Enemy.defeated


class Friend(Creature):
    def __init__(self, name: str, description: str = None) -> None:
        super().__init__(name, description)
        self.aggressive = False

    def set_trading(self, trade: str, prize: object) -> None:
        self.trading = trade
        self.prize = prize

    def trade(self, trading: str) -> bool:
        return trading == self.trading

    def get_prize(self) -> object:
        return self.prize


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.backpack = []
        self.health = 3

    def take_item(self, item: object) -> None:
        self.backpack.append(item)

    def drop_item(self, item: object) -> None:
        self.backpack.remove(item)

    def get_defeated(self) -> None:
        self.health -= 1

    def get_health(self) -> int:
        return self.health

    def get_backpack(self) -> list:
        return list(self.backpack)

    def get_name(self) -> str:
        return self.name


class Item:
    def __init__(self, name: str, description: str = None) -> None:
        self.name = name
        self.description = description or None

    def set_description(self, description: str) -> None:
        self.description = description

    def describe(self) -> None:
        print(f"The [{self.name}] is here - {self.description}")

    def get_name(self) -> str:
        return self.name
