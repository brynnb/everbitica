import random

class Mob:
    def __init__(self, DB, DI):
        self.DB = DB
        self.DI = DI

class Player:
    def __init__(self, shielding, defensive):
        self.shielding = shielding
        self.defensive = defensive

def calculate_damage(mob, player):
    DB = mob.DB * (1 - player.shielding)
    DI = mob.DI * player.defensive
    dmg = DB + random.randint(1, 20) * DI
    return dmg

# Create a mob with DB = 1000 and DI = 200
mob = Mob(1000, 200)

# Create a player with 30% shielding and 50% defensive
player = Player(0.3, 0.5)

# Calculate damage
dmg = calculate_damage(mob, player)
print(f"Damage: {dmg}")


def print_combat_message(attacker, defender, damage, attack_type=None):
    if attack_type:
        print(f"{attacker} {attack_type} a {defender} for {damage} points of damage.")
    else:
        print(f"{attacker} attacks {defender} for {damage} points of damage.")



def calculate_damage(mob, player, attack_type=None):
    DB = mob.DB * (1 - player.shielding)
    DI = mob.DI * player.defensive
    dmg = DB + random.randint(1, 20) * DI
    print_combat_message(mob.__class__.__name__, player.__class__.__name__, dmg, attack_type)
    return dmg


dmg = calculate_damage(mob, player, 'slashes')

class Character:
    def __init__(self, level, strength, weapon_base, bonus_modifier, offense_skill, class_type):
        self.level = level
        self.strength = strength
        self.weapon_base = weapon_base
        self.bonus_modifier = bonus_modifier
        self.offense_skill = offense_skill
        self.class_type = class_type

    def calculate_damage(self):
        # Calculate average slash
        average_slash = (2 * self.weapon_base) + self.bonus_modifier + self.strength

        # Calculate damage cap based on level and class
        if self.class_type == 'Caster':
            if self.level <= 9:
                damage_cap = 6
            elif self.level <= 19:
                damage_cap = 10
            elif self.level <= 29:
                damage_cap = 12
            elif self.level <= 39:
                damage_cap = 18
            else:
                damage_cap = 20
        elif self.class_type == 'Priest':
            if self.level <= 9:
                damage_cap = 9
            elif self.level <= 19:
                damage_cap = 12
            elif self.level <= 29:
                damage_cap = 20
            elif self.level <= 39:
                damage_cap = 26
            else:
                damage_cap = 40
        else:  # Melee & Tank
            if self.level <= 9:
                damage_cap = 10
            elif self.level <= 19:
                damage_cap = 14
            elif self.level <= 29:
                damage_cap = 30
            elif self.level <= 39:
                damage_cap = 60
            else:
                damage_cap = 100

        # Calculate main hand and off hand damage
        main_hand = min(average_slash * 2, damage_cap)
        off_hand = min(average_slash, damage_cap)

        # Add bonus damage for levels 28 and above
        if self.level >= 28:
            main_hand += (self.level - 28) // 3 + 1
            off_hand += (self.level - 28) // 3 + 1

        return main_hand, off_hand
    

# Create a character
char = Character(level=50, strength=250, weapon_base=10, bonus_modifier=0, offense_skill=200, class_type='Melee')

# Calculate damage
main_hand, off_hand = char.calculate_damage()
print(f"Main Hand Damage: {main_hand}")
print(f"Off Hand Damage: {off_hand}")