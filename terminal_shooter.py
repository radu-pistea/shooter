import sys,time, subprocess, random


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

    def __repr__(self):
        return self.id

class TextColors:
    red = "\u001b[0;31m"
    green = "\u001b[0;32m"
    yellow = "\u001b[0;33m"
    end = "\u001b[0m"


# Global variables
game_name = """
██╗  ██╗██╗██╗     ██╗     ██╗    ██╗ █████╗ ██╗   ██╗███████╗
██║ ██╔╝██║██║     ██║     ██║    ██║██╔══██╗██║   ██║██╔════╝
█████╔╝ ██║██║     ██║     ██║ █╗ ██║███████║██║   ██║█████╗  
██╔═██╗ ██║██║     ██║     ██║███╗██║██╔══██║╚██╗ ██╔╝██╔══╝  
██║  ██╗██║███████╗███████╗╚███╔███╔╝██║  ██║ ╚████╔╝ ███████╗
╚═╝  ╚═╝╚═╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝  ╚═══╝  ╚══════╝"""
t=TextColors
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

def typewriter_w(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        if char != "/n":
            time.sleep(0.05)
        else:
            time.sleep(1)

def typewriter(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.1)

def clear_screen():
    operating_system = sys.platform
    if operating_system == "win32":
        subprocess.run("cls", shell=True)
    elif operating_system == "linux" or operating_system == "darwin":
        subprocess.run("clear", shell=True)

# Define gift method at end of round
def gift():
    rand_gift = random.randint(1, 13)
    if rand_gift in gifts.keys():
        if gifts[rand_gift] in list(gift_equivalent.keys())[:2]:
            player.heal[len(player.heal)+1] = gifts[rand_gift]
            print(f"\nYou received a {t.green}{gifts[rand_gift]}{t.end} potion.")
        elif gifts[rand_gift] in list(gift_equivalent.keys())[2:]:
            gift = gift_equivalent[gifts[rand_gift]]
            player.armor += gift
            print(f"\n{gift} armour gained.")
        else:
            print("\nNo gift equivalent for you!")
    else:
        print("\nSorry! No gift for you! :(")

# Define stealth method
def stealth():
    clear_screen()
    global stealth_count
    random_stealth = random.randint(1, 100)
    if random_stealth <= Player.stealth:
        print(f"{t.green}\nSuccessful stealth! Enemy attack missed!{t.end}")
        stealth_count += 1
        if stealth_count == 5:
            Player.stealth += 5
            stealth_count = 0
        endround()
    else:
        print(f"{t.red}\nYou have been found!{t.end}")
        ai_turn()
        endround()

# Define function to roll dice
def roll_attack_dice():
    return random.randint(1, 3)

def roll_defender_dice():
    return random.randint(1, 2)

# Define function to calculate player damage
def calculate_player_damage(attack_dice, defender_dice, weapon_level):
    damage = (attack_dice - defender_dice) * (Player.damage * weapon_level)
    return damage

# Define function to calculate enemy damage
def calculate_enemy_damage(attack_dice, defender_dice):
    damage = (attack_dice - defender_dice) * Enemy.damage
    return damage

# Define endround logic
def endround():
    # global enemy_count, stealth_count
    # if player.hp <= 0:
    #     clear_screen()
    #     typewriter_w(f"{t.red}YOU DIED!\nKill Count: {player.kill_count}{t.end}\n")
    #     enemy_count = 1
    #     stealth_count = 0
    #     player.heal.clear()
    #     time.sleep(1)
    # else:
    gift()
    if player.armor > 100:
        player.armor = 100
    input("\nPress Enter to continue...")


# Define ai turn
def ai_turn():
    global attack_multiplier
    while True:
        attack_dice = roll_attack_dice()
        defender_dice = roll_defender_dice()
        print("\n-----Enemy's turn-----")
        print(f"Attack dice: {attack_dice}")
        print(f"Defender dice: {defender_dice}")
        if attack_dice == defender_dice:
            attack_multiplier += 1
            print("\nBonus damage multiplier X" + str(attack_multiplier))
        elif attack_dice < defender_dice:
            print(f"{t.red}\nAttack missed!{t.end}")
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
            print(f"{t.green}\nAttack hit: {damage} dmg{t.end}")
            attack_multiplier = 1
            break

# Define players turn
def player_turn():
    global attack_multiplier, enemy
    while True:
        attack_dice = roll_attack_dice()
        defender_dice = roll_defender_dice()
        clear_screen()
        print(f"\n-----{player.name}'s attack-----\n")
        print(f"Attack dice: {attack_dice}")
        print(f"Defender dice: {defender_dice}")
        if attack_dice == defender_dice:
            attack_multiplier += 1
            print("\nBonus damage multiplier X" + str(attack_multiplier))
        elif attack_dice < defender_dice:
            print(f"{t.red}\nAttack missed!{t.end}")
            attack_multiplier = 1
            ai_turn()
            endround()
            break
        else:
            damage = attack_multiplier * calculate_player_damage(attack_dice, defender_dice, Player.weapon_level)
            enemy.hp -= damage
            print(f"{t.green}\nAttack hit: {damage} dmg{t.end}")
            attack_multiplier = 1
            if enemy.hp <= 0:
                player.kill_count += 1
                Player.weapon_level = int((player.kill_count / 5) + 1)
                enemy = Enemy()
            ai_turn()
            endround()
            break

# Define healing logic
def heal():
    clear_screen()
    if len(player.heal) == 0:
        clear_screen()
        print("Your inventory is empty!")
        input("\nPress Enter to continue...")
    else:
        while True:
            print(f"Choose a healing potion:")
            print(player.heal)
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
        
# Print stats
def stats():
    print(f"------------Wave {enemy.id}------------")
    print(f"""
HP: {player.hp}/{player.max_hp}
Armour: {player.armor}/{player.max_armor}
Weapon Level: {player.weapon_level}
Stealth: {player.stealth}%
Kill Count: {player.kill_count}
Enemy HP: {enemy.hp}/100""")

# Menu and game

while True:
    clear_screen()
    print(game_name)
    print("\nMenu:\n")
    print("1. Start")
    print("2. Instructions\n")
    choice = input("Enter your choice: ")
    if choice == "1":
        player = Player(input("Enter your name: "))
        typewriter_w(f"\nWelcome {t.green}{player.name}{t.end}! Let's begin!\n")
        time.sleep(1.5)
        enemy = Enemy()
        player.kill_count = 0
        while True:
            clear_screen()
            if player.hp > 0:
                stats()
                print("\n1. Attack")
                print("2. Heal")
                print("3. Hide")
                player_choice = input("\nEnter your choice: ")
                if player_choice == "1":
                    player_turn()
                elif player_choice == "2":
                    heal()
                elif player_choice == "3":
                    stealth()
                elif player_choice.lower() == "quit":
                    break
                else:
                    print("\nInvalid choice. Try again.")
                    input("\nPress Enter to continue...")
            else:

                clear_screen()
                typewriter_w(f"{t.red}YOU DIED!\nKill Count: {player.kill_count}{t.end}\n")
                enemy_count = 1
                stealth_count = 0
                player.heal.clear()
                time.sleep(1)
                input("\nPress Enter to continue...")
                break

    elif choice == "2":
        clear_screen()
        print("""
        Welcome to the Text-Based Shooter Game! Here's how to play:

1. Your objective is to survive as long as possible and eliminate as many enemies as you can.
2. The game is divided into rounds, each consisting of a player's turn and an enemy's turn.
3. During your turn, you can choose from the following actions:
   - Attack: Roll an attack dice (1-3) to determine your attack strength.
   - Heal: Restore your health by a fixed amount (e.g., 25).
   - Hide: Attempt to hide from enemy attacks (initial 10% chance).
4. After your turn, it's the enemy's turn. The enemy attacks, and the dices are rolled randomly.
5. Attack Calculation:
   - If your attack dice < defender dice, your attack misses.
   - If dice rolls are equal, a bonus multiplier increases.
   - If your attack dice > defender dice, damage is calculated as follows:
     Damage = (attack dice - defender dice) * base attack * weapon level * bonus multiplier.
6. Subtract enemy attack damage from your health.
7. Check if your health drops to 0 or below. If so, the game ends.
8. After each round, you may receive a gift: healing potions or armor.
9. Use healing potions from the healing menu to restore health.
10. After every 5 kills, your weapon level increases by 1.
11. Keep track of your score, which increases with each surviving round.
12. Game continues until your health reaches 0 or you decide to quit.
13. If you choose to "hide":
   - You have a starting 10% chance of not being found.
   - After 5 successful stealths, your stealth chance increases by 5%.
   
Enjoy the game, and good luck!
Have fun and challenge yourself to achieve the highest score!""")
        input("\nPress Enter to continue...")



    elif choice.lower() == "quit":
        break
    else:
        print("\nInvalid choice. Try again.")
        input("\nPress Enter to continue...")

