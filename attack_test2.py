import time
import random

class Character:
    def __init__(self, name, level, strength, weapon_base, bonus_modifier):
        self.name = name
        self.hp = 100
        self.level = level
        self.strength = strength
        self.weapon_base = weapon_base
        self.bonus_modifier = bonus_modifier

    def is_alive(self):
        return self.hp > 0

    def calculate_damage(self):
        # Replace this with your actual damage calculation
        return (2 * self.weapon_base) + self.bonus_modifier + self.strength

    def attack(self, other):
        damage = self.calculate_damage()
        other.hp -= damage
        print(f"{self.name} attacks {other.name} for {damage} damage. {other.name} has {other.hp} HP left.")

# Create PC and NPC with level, strength, weapon base, and bonus modifier
pc = Character("Owlie", 3, 12, 6, 0)
npc = Character("An orc guard", 1, 10, 5, 0)

# Battle loop
while pc.is_alive() and npc.is_alive():
    pc.attack(npc)
    time.sleep(3)
    if npc.is_alive():
        npc.attack(pc)
        time.sleep(3)

# Print result
if pc.is_alive():
    print("PC wins!")
else:
    print("NPC wins!")