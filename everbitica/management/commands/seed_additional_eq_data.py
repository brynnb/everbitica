from django.core.management.base import BaseCommand
from everbitica.models import *


class Command(BaseCommand):
    """
    Seeds the database with additional EQ data that isn't in the original SQL import. 
    This data includes info such as character classes and deities which is hardcoded into the original EQ client and isn't explicitly labeled in the database, at least not that I can tell
    """

    help = (
        "Seeds the database with additional EQ data that isn't in original SQL import"
    )

    def handle(self, *args, **options):
        classes = [
            (1, 1, "Warrior", None),
            (2, 2, "Cleric", 1),
            (3, 4, "Paladin", 8),
            (4, 8, "Ranger", 10),
            (5, 16, "Shadow Knight", 9),
            (6, 32, "Druid", 7),
            (7, 64, "Monk", None),
            (8, 128, "Bard", 11),
            (9, 256, "Rogue", None),
            (10, 512, "Shaman", 6),
            (11, 1024, "Necromancer", 3),
            (12, 2048, "Wizard", 2),
            (13, 4096, "Magician", 4),
            (14, 8192, "Enchanter", 5),
            (15, 16384, "Beastlord", 12),
            (16, 32768, "Berserker", None),
            (17, None, "Banker", None),
            (20, None, "GM Warrior", None),
            (21, None, "GM Cleric", None),
            (22, None, "GM Paladin", None),
            (23, None, "GM Ranger", None),
            (24, None, "GM Shadow Knight", None),
            (25, None, "GM Druid", None),
            (26, None, "GM Monk", None),
            (27, None, "GM Bard", None),
            (28, None, "GM Rogue", None),
            (29, None, "GM Shaman", None),
            (30, None, "GM Necromancer", None),
            (31, None, "GM Wizard", None),
            (32, None, "GM Magician", None),
            (33, None, "GM Enchanter", None),
            (34, None, "GM Beastlord", None),
            (35, None, "GM Berserker", None),
            (40, None, "Banker", None),
            (41, None, "Shopkeeper", None),
            (59, None, "Discord Merchant", None),
            (60, None, "Adventure Recruiter", None),
            (61, None, "Adventure Merchant", None),
            (63, None, "Tribute Master", None),
            (64, None, "Guild Tribute Master", None),
            (66, None, "Guild Bank", None),
            (67, None, "Radiant Crystal Merchant", None),
            (68, None, "Ebon Crystal Merchant", None),
            (69, None, "Fellowships", None),
            (70, None, "Alternate Currency Merchant", None),
            (71, None, "Mercenary Merchant", None),
        ]
        for class_data in classes:
            CharacterClass.objects.create(
                id=class_data[0],
                bitmask=class_data[1],
                name=class_data[2],
                spell_list_id=class_data[3],
            )

        deities = [
            (1, "Bertoxxulos"),
            (2, "Brell Serilis"),
            (3, "Cazic Thule"),
            (4, "Erollisi Marr"),
            (5, "Bristlebane"),
            (6, "Innoruuk"),
            (7, "Karana"),
            (8, "Mithaniel Marr"),
            (9, "Prexus"),
            (10, "Quellious"),
            (11, "Rallos Zek"),
            (12, "Rodcet Nife"),
            (13, "Solusek Ro"),
            (14, "The Tribunal"),
            (15, "Tunare"),
            (16, "Veeshan"),
        ]
        for deity in deities:
            Deity.objects.create(id=deity[0], name=deity[1])

        self.stdout.write(self.style.SUCCESS("Successfully seeded additional EQ data!"))
