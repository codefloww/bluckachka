"""main module of the game"""

from curses.ascii import isalnum, isdigit
import blukachka.game as game


class Blukachka:
    def __init__(self) -> None:
        self.running = False

    def play(self):
        self.running = True
        self._session()

    def _create_game_world(self):
        flyer = game.Item("flyer", "Some useless paper")
        bottle = game.Item("bottle", "A delicious bottle of water")
        gun = game.Item("gun", "Realy dangerous weapon")
        book = game.Item("book", "Super boring school book")
        croissant = game.Item("croisant", "Smells so good")
        money = game.Item("money", "A good one, may be useful")

        univercity = game.Street("Kozelnytska St.", "Yeah, my university")
        park = game.Street("Striyskiy park", "Really nice park")
        center = game.Street("Svobody Av.", "Center of the Lviv")
        zelena = game.Street("Zelena St.")
        chornovola = game.Street("Chornovola St.")
        lypynskoho = game.Street("Lypynskoho St.", "nothing too interesting")
        novozn = game.Street(
            "Novoznesenska St.", "I think I know this street pretty well)"
        )
        syhiv = game.Street("Syhiv", "Hardcore")

        pupil = game.Friend("Andrii", "Some annoying kid, looking for something")
        drunk = game.Enemy("Drunk man", "bwoah, smells so bad")
        kacap = game.Enemy("russian", "The typical as***le")
        woman = game.Enemy("Babka", "Very very angry old woman")
        kid = game.Friend("Orest", "hehehe, not ork")
        zbui = game.Enemy("Gopnik", "Not that enjoyable person")

        self.current_street = univercity
        univercity.set_item(flyer)
        park.set_item(bottle)
        center.set_item(croissant)
        pupil.add_replique("OOO, hiiiii")
        pupil.add_replique("Have you seen my book?")
        pupil.add_replique("What have you told about me?")
        pupil.set_trading("book", gun)
        park.set_creature(pupil)

        drunk.add_replique("Bwoahakabla")
        drunk.add_replique("OAOH GO FROM HeRe You liTtle...")
        drunk.set_weakness("bottle")
        zelena.set_creature(drunk)
        zelena.set_item(book)

        kacap.set_weakness("gun")
        kacap.add_replique("Crimea is ours!")
        kacap.add_replique("Putin is the best!")
        chornovola.set_creature(kacap)

        woman.add_replique("What are you doing here???")
        woman.add_replique("Moove on!!!")
        woman.add_replique("Be quiter!!!!")
        woman.add_replique("You aRe So uncuLtuRed")
        woman.set_weakness("flyer")
        lypynskoho.set_creature(woman)

        kid.set_trading("bottle", money)
        kid.add_replique("Hello!")
        kid.add_replique("Wanna play football?")
        kid.add_replique("Wow, you're playing very good")
        kid.add_replique("I'm tired from playing, do you have anything to drink?")
        novozn.set_creature(kid)

        zbui.add_replique("HAHAHAHA")
        zbui.add_replique("Where your phone?")
        zbui.set_weakness("money")
        syhiv.set_creature(zbui)

        univercity.link_streets(park)
        park.link_streets(zelena)
        park.link_streets(center)
        chornovola.link_streets(center)
        chornovola.link_streets(lypynskoho)
        lypynskoho.link_streets(novozn)
        syhiv.link_streets(univercity)

    def _session(self):
        self._create_game_world()
        player_name = input("Type your name: ")
        player = game.Player(player_name)
        print(f"Welcome to Lviv {player.name}")
        while self.running:
            print("\n")
            self.current_street.describe()
            inhabitants = self.current_street.get_creatures_by_names()
            if inhabitants:
                print("You can see some figures here:")
                for creature in inhabitants.values():
                    creature.describe()

            items = self.current_street.get_items_by_names()
            if items:
                print("Look closer, there are some items:")

                for item in items.values():
                    item.describe()

            command = input("> ")

            if command in self.current_street.get_nearby_streets():
                self.current_street = self.current_street.move(command)
            elif command.isdigit() and 0 < int(command) <= len(
                self.current_street.get_nearby_streets()
            ):
                self.current_street = self.current_street.move(
                    self.current_street.get_nearby_streets()[int(command) - 1]
                )

            elif command == "talk":
                if len(inhabitants) > 1:
                    dialoguer = input("Choose a inhabitant to speak to: ")
                    if dialoguer in inhabitants:
                        inhabitants[dialoguer].talk()
                    else:
                        print("There is no such inhabitant")
                elif len(inhabitants) == 1:
                    list(inhabitants.values())[0].talk()
                else:
                    print(f"Emmmm, {player.get_name()}, you're talking to yourself")

            elif command == "fight":
                if inhabitants:
                    print("Choose your enemy:")
                    fight_against = input()
                    print("What will you fight with?")
                    fight_with = input()

                    # Do I have this item?
                    if fight_with in player.backpack:
                        if fight_against not in inhabitants:
                            print("Hmmm, who are you fighting???")
                        elif inhabitants[fight_against].is_enemy() and inhabitants[
                            fight_against
                        ].fight(fight_with):
                            # What happens if you win?
                            print("Hooray, you won the fight!")
                            self.current_street.remove_creature(
                                inhabitants[fight_against]
                            )
                            if inhabitants[fight_against].get_defeated() == 4:
                                print(
                                    "Congratulations, you have vanquished the enemy horde!"
                                )
                                self.running = False
                        elif not inhabitants[fight_against].is_enemy():
                            print(
                                "Nooo, this one is friendly, why'd you want to fight?"
                            )
                        else:
                            # What happens if you lose?
                            print("Oh dear, you lost the fight.")
                            if player.get_health() > 1:
                                print("Be more careful!")
                                player.get_defeated()
                            else:
                                print("Ooooh no, you sadly died(")
                                self.running = False
                    else:
                        print("You don't have a " + fight_with)
                else:
                    print("Are you trying to fight with yourself?)))")
            elif command == "take":
                if len(player.get_backpack()) > 2:
                    print("You have too many things in backpack!")
                elif len(items) > 1:

                    taken_item = input("Which item do you want to take: ")
                    if taken_item in items:
                        print("You put the " + taken_item + " in your backpack")
                        player.take_item(taken_item)
                        self.current_street.remove_item(items[taken_item])
                    else:
                        print("There is no such item on street!")

                elif len(items) == 1:
                    print("You put the " + list(items.keys())[0] + " in your backpack")
                    player.take_item(list(items.keys())[0])
                    self.current_street.remove_item(list(items.values())[0])
                else:
                    print("You have nothing to take here")

            elif command == "trade":
                for inhabitant in inhabitants:
                    if not inhabitants[inhabitant].is_enemy():
                        print(f"What you want to trade with {inhabitant}?")
                        trading = input()
                        if trading not in player.get_backpack():
                            print("You don't have such item")
                        else:
                            if inhabitants[inhabitant].trade(trading):
                                prize = inhabitants[inhabitant].get_prize()
                                player.take_item(prize.get_name())
                                inhabitants[inhabitant].set_trading(None, None)
                                print(
                                    f"You got the {prize.get_name()} from {inhabitant}"
                                )
                                player.drop_item(trading)

                            else:
                                print(f"{inhabitant} doesn't want this")

            elif command == "drop":
                print("Which item you want to drop?")
                dropping = input()
                player.drop_item(dropping)

            elif command == "backpack":
                print(f"You have in backpack: {player.get_backpack()}")

            elif command == "help":
                print("\n\n")
                print(
                    """You have several options to do:
> talk
In such way you can talk to inhabitants
> take
You can take some items on street
> <name of the street>
You can move to another streets
> fight
You can fight with your enemies
> help
You can have guidence on options
> exit
You can exit the game
> trade
You can trade items with friends
> drop
You can drop things when your backpack is too heavy
> backpack
You can see what you have in your backpack"""
                )
            elif command == "exit":
                print(
                    f"Goodbye {player.get_name()}, sadly that you haven't finished the game((("
                )
                exit()
            else:
                print("I don't know how to " + command)


if __name__ == "__main__":
    best_game = Blukachka()
    best_game.play()
