import random

# Global variables
stealth_count = 0
enemy_count = 1
attack_multiplier = 1
gifts = {
    1: "Basic Healing",
    2: "Basic Healing",
    3: "Superior healing",
    4: "Basic armour",
    6: "Basic Healing",
    7: "Basic Healing"
}
gift_equivalent = {"Basic Healing": 25, "Superior healing": 50, "Basic armour": 25, "Superior armour": 50}

# Define gift method at end of round
def gift():
    rand_gift = random.randint(1, 13)
    if rand_gift in gifts.keys():
        if gifts[rand_gift] in list(gift_equivalent.keys())[:2]:
            player.heal[len(player.heal)+1] = gifts[rand_gift]
            print(f"You received a {gifts[rand_gift]} potion.")
        elif gifts[rand_gift] in list(gift_equivalent.keys())[2:]:
            gift = gift_equivalent[gifts[rand_gift]]
            player.armor += gift
            print(f"{gift} armour gained.")
        else:
            print("No gift equivalent for you!")
    else:
        print("Sorry! No gift for you! :(")

def stealth():
    global stealth_count
    random_stealth = random.randint(1, 100)
    if random_stealth <= Player.stealth:
        print("Successful stealth! Enemy attack missed!")
        stealth_count += 1
        if stealth_count == 5:
            Player.stealth += 5
            stealth_count = 0
        endround()
    else:
        print("You have been found!")
        ai_turn()
        endround()







# Player class with stats
class Player:
    hp = 100
    max_hp = 100
    armor = 0
    max_armor = 100
    weapon_level = 1
    stealth = 10
    max_stealth = 75
    kill_count = 0
    damage = 25
    heal = {}

    def __init__(self, name):
        self.name = name


# Enemy class
class Enemy:
    hp = 100
    damage = 10
    def __init__(self):
        global enemy_count
        self.id = enemy_count
        enemy_count += 1

# Define function to roll dice
def roll_dice():
    return random.randint(1, 6)

# Define function to calculate player damage
def calculate_player_damage(attack_dice, defender_dice, weapon_level):
    damage = (attack_dice - defender_dice) * (Player.damage * weapon_level)
    return damage

# Define function to calculate player damage
def calculate_enemy_damage(attack_dice, defender_dice):
    damage = (attack_dice - defender_dice) * Enemy.damage
    return damage

def endround():
    global enemy_count, stealth_count
    if player.hp <= 0:
        print(f"You died! Kill Count: {player.kill_count}")
        enemy_count = 1
        stealth_count = 0
        player.heal.clear()
    else:
        gift()
    if player.armor > 100:
        player.armor = 100

# Define ai turn
def ai_turn():
    global attack_multiplier
    while True:
        attack_dice = roll_dice()
        defender_dice = roll_dice()
        print("\n-----------------")
        print("Enemy's turn:")
        print(f"Attack dice: {attack_dice}")
        print(f"Defender dice: {defender_dice}")
        print("-----------------")
        if attack_dice == defender_dice:
            attack_multiplier += 1
            print("\nBonus damage multiplier X" + str(attack_multiplier))
        elif attack_dice < defender_dice:
            print("\nAttack missed!")
            attack_multiplier = 1
            break
        else:
            damage = attack_multiplier * calculate_enemy_damage(attack_dice, defender_dice)
            if player.armor > 0:
                if player.armor - damage / 2 <= 0:
                    damage -= player.armor * 2
                    player.armor = 0
                    player.hp -= damage
                elif player.armor - damage / 2 > 0:
                    player.armor -= int(damage / 2)
            else:
                player.hp -= damage
            print(f"\nAttack hit: {damage} dmg")
            attack_multiplier = 1
            break


# Menu

while True:
    print("\nMenu:")
    print("1. Start")
    choice = input("Enter your choice: ")
    if choice == "1":
        player = Player(input("Enter your name: "))
        print(f"\nWelcome {player.name}! Let's begin!")
        enemy = Enemy()
        player.kill_count = 0
        while player.hp > 0:
            print("\nOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
            print(f"Wave {enemy.id}:")
            print("1. Attack")
            print("2. Heal")
            print("3. Hide")
            print(f"HP: {player.hp}/{player.max_hp} | Armour: {player.armor}/{player.max_armor} | Weapon Level: {player.weapon_level} | Stealth: {player.stealth}% | Kill Count: {player.kill_count} | Enemy HP: {enemy.hp}/100")
            print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
            player_choice = input("\nEnter your choice: ")
            if player_choice == "1":
                while True:
                    attack_dice = roll_dice()
                    defender_dice = roll_dice()
                    print("\n-----------------")
                    print(f"Attack dice: {attack_dice}")
                    print(f"Defender dice: {defender_dice}")
                    print("-----------------")
                    if attack_dice == defender_dice:
                        attack_multiplier += 1
                        print("\nBonus damage multiplier X" + str(attack_multiplier))
                    elif attack_dice < defender_dice:
                        print("\nAttack missed!")
                        attack_multiplier = 1
                        ai_turn()
                        endround()
                        break
                    else:
                        damage = attack_multiplier * calculate_player_damage(attack_dice, defender_dice, Player.weapon_level)
                        enemy.hp -= damage
                        print(f"\nAttack hit: {damage} dmg")
                        attack_multiplier = 1
                        if enemy.hp <= 0:
                            player.kill_count += 1
                            enemy = Enemy()
                        ai_turn()
                        endround()
                        break
            elif player_choice == "2":
                if len(player.heal) == 0:
                    print("Your inventory is empty!")
                else:
                    while True:
                        print("\n-----------------")
                        print(f"Choose a healing potion:")
                        print(player.heal)
                        print("-----------------")
                        choice = input("\nEnter your choice: ")
                        if int(choice) in player.heal:
                            player.hp += gift_equivalent[player.heal[int(choice)]]
                            player.heal.pop(int(choice))
                            break
                        else:
                            print("Invalid choice. Try again.")
                    if player.hp > 100:
                        player.hp = 100
                    ai_turn()
                    endround()
            elif player_choice == "3":
                stealth()
            elif player_choice.lower() == "quit":
                break
    elif choice.lower() == "quit":
        break
    else:
        print("Invalid choice. Try again.")

