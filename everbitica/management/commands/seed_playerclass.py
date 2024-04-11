from django.core.management.base import BaseCommand
from everbitica.models import PlayerClass

class Command(BaseCommand):
    help = 'Seeds the database with PlayerClass instances'

    def handle(self, *args, **options):
        class_data = {
            0: ("Warrior", "The quintessential tank class, excelling in melee combat and able to withstand significant amounts of damage.", False),
            1: ("Warrior", "The quintessential tank class, excelling in melee combat and able to withstand significant amounts of damage.", True),
            2: ("Cleric", "Powerful healers devoted to their deity, wielding divine magic to heal and resurrect allies.", True),
            3: ("Paladin", "Holy warriors blending combat prowess with divine magic, focusing on healing, protection, and smiting undead.", True),
            4: ("Ranger", "Versatile warriors of nature, adept with both the bow and sword, and able to cast nature-based spells.", True),
            5: ("Shadow Knight", "Dark knights who blend the arts of combat and necromancy, excelling in fear, disease, and summoning undead minions.", True),
            6: ("Druid", "Nature-based spellcasters with the ability to heal, teleport, and call upon elemental forces.", True),
            7: ("Monk", "Martial artists who excel in hand-to-hand combat and can dodge and feign death to avoid damage.", True),
            8: ("Bard", "Master musicians capable of casting spells by weaving magical songs.", True),
            9: ("Rogue", "Stealthy and dexterous fighters specializing in dual-wielding, backstabbing, and lockpicking.", True),
            10: ("Shaman", "Spiritual guides and practitioners of mystic arts, capable of healing, buffing, and cursing.", True),
            11: ("Necromancer", "Dark spellcasters who summon undead minions, leech life from enemies, and can become powerful summoners of death.", True),
            12: ("Wizard", "Powerful spellcasters focusing on direct damage spells and teleportation magic.", True),
            13: ("Magician", "Summoners who can conjure elemental minions, weapons, and items to assist in battle.", True),
            14: ("Enchanter", "Master manipulators of the mind, capable of charming, mesmerizing, and debuffing enemies.", True),
            15: ("Beastlord", "Warriors who bond with a beast companion, combining melee and magical skills.", False),
            16: ("Berserker", "A fierce warrior class that excels in rage-fueled combat.", False),
            17: ("Banker", "", False),
            20: ("GM Warrior", "", False),
            21: ("GM Cleric", "", False),
            22: ("GM Paladin", "", False),
            23: ("GM Ranger", "", False),
            24: ("GM Shadow Knight", "", False),
            25: ("GM Druid", "", False),
            26: ("GM Monk", "", False),
            27: ("GM Bard", "", False),
            28: ("GM Rogue", "", False),
            29: ("GM Shaman", "", False),
            30: ("GM Necromancer", "", False),
            31: ("GM Wizard", "", False),
            32: ("GM Magician", "", False),
            33: ("GM Enchanter", "", False),
            34: ("GM Beastlord", "", False),
            35: ("GM Berserker", "", False),
            40: ("Banker", "", False),
            41: ("Shopkeeper", "", False),
            59: ("Discord Merchant", "", False),
            60: ("Adventure Recruiter", "", False),
            61: ("Adventure Merchant", "", False),
            63: ("Tribute Master", "", False),
            64: ("Guild Tribute Master", "", False),
            66: ("Guild Bank", "", False),
            67: ("Radiant Crystal Merchant", "", False),
            68: ("Ebon Crystal Merchant", "", False),
            69: ("Fellowships", "", False),
            70: ("Alternate Currency Merchant", "", False),
            71: ("Mercenary Merchant", "", False),
        }


        for id, (name, description, is_playable) in class_data.items():
            PlayerClass.objects.create(id=id, name=name, description=description, is_playable=is_playable)

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with PlayerClass instances'))