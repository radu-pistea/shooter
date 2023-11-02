import random

# Global variables

enemy_count = 1
attack_multiplier = 1
gifts = {1: "Basic Healing", 2: "Basic Healing", 3: "Superior healing", 4: "Basic armour", 5: "Superior armour"}
gift_equivalent = {"Basic Healing": 25, "Superior healing": 50, "Basic armour": 25, "Superior armour": 50}

# Define gift method at end of round
def gift():
    rand_gift = random.randint(1, 10)
    if rand_gift in gifts.keys():
        if gifts[rand_gift] in list(gift_equivalent.keys())[:2]:
            player.heal[gifts[rand_gift]] = gift_equivalent[gifts[rand_gift]]
            print(f"You received a {gifts[rand_gift]} potion.")
        elif gifts[rand_gift] in list(gift_equivalent.keys())[2:]:
            gift = gift_equivalent[gifts[rand_gift]]
            player.armor += gift
            print(f"{gift} armour gained.")
        else:
            print("No gift equivalent for you!")
    else:
        print("Sorry! No gift for you! :(")

# Player class with stats
class Player:
    hp = 100
    max_hp = 100
    armor = 0
    max_armor = 100
    weapon_level = 1
    stealth = 0
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
    if player.hp <= 0:
        print(f"You died! Kill Count: {player.kill_count}")
    else:
        gift()
    if player.hp > 100:
        player.hp = 100
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
            print(f"HP: {player.hp}/{player.max_hp} | Armor: {player.armor}/{player.max_armor} | Weapon Level: {player.weapon_level} | Stealth: {player.stealth}% | Kill Count: {player.kill_count} | Enemy HP: {enemy.hp}/100")
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
    else:
        print("Invalid choice. Try again.")

