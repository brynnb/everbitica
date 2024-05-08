from django.test import TestCase
from .views import get_party_members
from .models import *
from django.core.management import call_command
from django.apps import apps
from django.db.models.fields.related import ForeignKey



# having issue with migration matching original table, trying to figure out discrepency
class TableTest(TestCase):
        #run SQL query to get all field names for the eq_items table
    def test_table(self):
        #get all field names for the eq_items table

        fields = Item._meta.get_fields()
        field_names = [field.name for field in fields if field.get_internal_type() != 'ForeignKey']

        #print all field_names
        print(field_names)
        
        original_field_names = [
            'id',
            'minstatus',
            'Name',
            'aagi',
            'ac',
            'acha',
            'adex',
            'aint',
            'asta',
            'astr',
            'awis',
            'bagsize',
            'bagslots',
            'bagtype',
            'bagwr',
            'banedmgamt',
            'banedmgbody',
            'banedmgrace',
            'bardtype',
            'bardvalue',
            'book',
            'casttime',
            'casttime_',
            'classes',
            'color',
            'price',
            'cr',
            'damage',
            'deity',
            'delay',
            'dr',
            'clicktype',
            'clicklevel2',
            'elemdmgtype',
            'elemdmgamt',
            'factionamt1',
            'factionamt2',
            'factionamt3',
            'factionamt4',
            'factionmod1',
            'factionmod2',
            'factionmod3',
            'factionmod4',
            'filename',
            'focuseffect',
            'fr',
            'fvnodrop',
            'clicklevel',
            'hp',
            'icon',
            'idfile',
            'itemclass',
            'itemtype',
            'light',
            'lore',
            'magic',
            'mana',
            'material',
            'maxcharges',
            'mr',
            'nodrop',
            'norent',
            'pr',
            'procrate',
            'races',
            'range',
            'reclevel',
            'recskill',
            'reqlevel',
            'sellrate',
            'size',
            'skillmodtype',
            'skillmodvalue',
            'slots',
            'clickeffect',
            'tradeskills',
            'weight',
            'booktype',
            'recastdelay',
            'recasttype',
            'updated',
            'comment',
            'stacksize',
            'stackable',
            'proceffect',
            'proctype',
            'proclevel2',
            'proclevel',
            'worneffect',
            'worntype',
            'wornlevel2',
            'wornlevel',
            'focustype',
            'focuslevel2',
            'focuslevel',
            'scrolleffect',
            'scrolltype',
            'scrolllevel2',
            'scrolllevel',
            'serialized',
            'verified',
            'serialization',
            'source',
            'lorefile',
            'questitemflag',
            'clickunk5',
            'clickunk6',
            'clickunk7',
            'procunk1',
            'procunk2',
            'procunk3',
            'procunk4',
            'procunk6',
            'procunk7',
            'wornunk1',
            'wornunk2',
            'wornunk3',
            'wornunk4',
            'wornunk5',
            'wornunk6',
            'wornunk7',
            'focusunk1',
            'focusunk2',
            'focusunk3',
            'focusunk4',
            'focusunk5',
            'focusunk6',
            'focusunk7',
            'scrollunk1',
            'scrollunk2',
            'scrollunk3',
            'scrollunk4',
            'scrollunk5',
            'scrollunk6',
            'scrollunk7',
            'clickname',
            'procname',
            'wornname',
            'focusname',
            'scrollname',
            'created',
            'bardeffect',
            'bardeffecttype',
            'bardlevel2',
            'bardlevel',
            'bardunk1',
            'bardunk2',
            'bardunk3',
            'bardunk4',
            'bardunk5',
            'bardname',
            'bardunk7',
            'gmflag',
            'soulbound'
        ]

     

class ItemModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        call_command('seed_eq_data_tables')
        call_command('seed_additional_eq_data')
        super().setUpClass()

    def test_item_creation(self):
        item = Item.objects.get(id=1001)
        self.assertEqual(item.name, "Cloth Cap")
        self.assertEqual(item.ac, 2)
        self.assertEqual(item.price, 200)
    
class TestEQFeatures(TestCase):
    #create CharacterData then create and associated CharacterCurrency, CharacterInventory, CharacterSpells (pick 8 at random from existing Spell model)

    @classmethod
    def setUpTestData(cls):
        # call_command('seed_eq_data_tables')
        # call_command('seed_additional_eq_data')
        cls.character = CharacterData.objects.create(name="Test Character")
        cls.currency = CharacterCurrency.objects.create(character_data=cls.character, platinum=100, gold=100, silver=100, copper=100)
        cls.inventory = CharacterInventory.objects.create(character_data=cls.character)

        #add 8 spells to the character
        spells = Spell.objects.all().order_by('?')[:8]
        for spell in spells:
            CharacterSpell.objects.create(character_data=cls.character, spell=spell)

    

    def test_features(self):
        self.assertEqual(CharacterData.objects.count(), 1)


# class GetPartyMembersTest(TestCase):

#     def test_get_party_members(self):
#         party_members = get_party_members()

#         # assert it's at least one long
#         self.assertTrue(len(party_members) > 0)

#         for member in party_members:
#             self.assertTrue("hp" in member)
#             self.assertTrue("mp" in member)
#             self.assertTrue("maxMP" in member)
#             self.assertTrue("maxHealth" in member)
#             self.assertTrue("username" in member)


# class BookModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         Book.objects.create(name="Test Book", txtfile="Test content")

#     def test_name_label(self):
#         book = Book.objects.get(id=1)
#         field_label = book._meta.get_field("name").verbose_name
#         self.assertEqual(field_label, "name")

#     def test_name_max_length(self):
#         book = Book.objects.get(id=1)
#         max_length = book._meta.get_field("name").max_length
#         self.assertEqual(max_length, 30)

#     def test_object_name_is_name(self):
#         book = Book.objects.get(id=1)
#         expected_object_name = f"{book.name}"
#         self.assertEqual(expected_object_name, str(book))

#     def test_txtfile_label(self):
#         book = Book.objects.get(id=1)
#         field_label = book._meta.get_field("txtfile").verbose_name
#         self.assertEqual(field_label, "txtfile")


# class FactionModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         Faction.objects.create(
#             id=1, name="Test Faction", base=0, see_illusion=True, min_cap=0, max_cap=0
#         )

#     def test_name_label(self):
#         faction = Faction.objects.get(id=1)
#         field_label = faction._meta.get_field("name").verbose_name
#         self.assertEqual(field_label, "name")

#     def test_name_max_length(self):
#         faction = Faction.objects.get(id=1)
#         max_length = faction._meta.get_field("name").max_length
#         self.assertEqual(max_length, 50)

#     def test_object_name_is_name(self):
#         faction = Faction.objects.get(id=1)
#         expected_object_name = f"{faction.name}"
#         self.assertEqual(expected_object_name, str(faction))

#     def test_base_default(self):
#         faction = Faction.objects.get(id=1)
#         default = faction._meta.get_field("base").default
#         self.assertEqual(default, 0)

#     def test_see_illusion_default(self):
#         faction = Faction.objects.get(id=1)
#         default = faction._meta.get_field("see_illusion").default
#         self.assertEqual(default, True)

#     def test_min_cap_default(self):
#         faction = Faction.objects.get(id=1)
#         default = faction._meta.get_field("min_cap").default
#         self.assertEqual(default, 0)

#     def test_max_cap_default(self):
#         faction = Faction.objects.get(id=1)
#         default = faction._meta.get_field("max_cap").default
#         self.assertEqual(default, 0)


# class LootdropModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         Lootdrop.objects.create(id=1, name="Test Lootdrop")

#     def test_name_label(self):
#         lootdrop = Lootdrop.objects.get(id=1)
#         field_label = lootdrop._meta.get_field("name").verbose_name
#         self.assertEqual(field_label, "name")

#     def test_name_max_length(self):
#         lootdrop = Lootdrop.objects.get(id=1)
#         max_length = lootdrop._meta.get_field("name").max_length
#         self.assertEqual(max_length, 255)


# class LootdropEntryModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         Lootdrop.objects.create(id=1, name="Test Lootdrop Entry")
#         LootdropEntry.objects.create(lootdrop_id=1, item_id=1)

#     def test_item_id_label(self):
#         entry = LootdropEntry.objects.get(id=1)
#         field_label = entry._meta.get_field("item_id").verbose_name
#         self.assertEqual(field_label, "item id")


# class LoottableModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         Loottable.objects.create(id=1, name="Test Loottable")

#     def test_name_label(self):
#         loottable = Loottable.objects.get(id=1)
#         field_label = loottable._meta.get_field("name").verbose_name
#         self.assertEqual(field_label, "name")

#     def test_name_max_length(self):
#         loottable = Loottable.objects.get(id=1)
#         max_length = loottable._meta.get_field("name").max_length
#         self.assertEqual(max_length, 255)


# class LoottableEntryModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         loottable = Loottable.objects.create(name="Test Loottable")
#         lootdrop = Lootdrop.objects.create(name="Test Lootdrop")
#         LoottableEntry.objects.create(loottable=loottable, lootdrop=lootdrop)

#     def test_loottable_label(self):
#         entry = LoottableEntry.objects.get(id=1)
#         field_label = entry._meta.get_field("loottable").verbose_name
#         self.assertEqual(field_label, "loottable")


# class ZoneModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         Zone.objects.create(
#             short_name="Test Zone",
#             long_name="This is a test zone",
#             id=1,
#             file_name="test_file",
#             map_file_name="test_map_file",
#             safe_x=0,
#             safe_y=0,
#             safe_z=0,
#             safe_heading=0,
#             graveyard_id=0,
#             min_level=0,
#             min_status=0,
#             zoneidnumber=0,
#             timezone=0,
#             maxclients=0,
#             ruleset=0,
#             note="Test note",
#             underworld=0,
#             minclip=450,
#             maxclip=450,
#             fog_minclip=450,
#             fog_maxclip=450,
#             fog_blue=0,
#             fog_red=0,
#             fog_green=0,
#             sky=1,
#             ztype=1,
#             zone_exp_multiplier=0.00,
#             gravity=0.4,
#             time_type=2,
#             fog_red1=0,
#             fog_green1=0,
#             fog_blue1=0,
#             fog_minclip1=450,
#             fog_maxclip1=450,
#             fog_red2=0,
#             fog_green2=0,
#             fog_blue2=0,
#             fog_minclip2=450,
#             fog_maxclip2=450,
#             fog_red3=0,
#             fog_green3=0,
#             fog_blue3=0,
#             fog_minclip3=450,
#             fog_maxclip3=450,
#             fog_red4=0,
#             fog_green4=0,
#             fog_blue4=0,
#             fog_minclip4=450,
#             fog_maxclip4=450,
#             fog_density=0,
#             flag_needed="",
#             canbind=1,
#             cancombat=1,
#             canlevitate=1,
#             castoutdoor=1,
#             hotzone=0,
#             shutdowndelay=5000,
#             peqzone=1,
#             expansion=0,
#             suspendbuffs=0,
#             rain_chance1=0,
#             rain_chance2=0,
#             rain_chance3=0,
#             rain_chance4=0,
#             rain_duration1=0,
#             rain_duration2=0,
#             rain_duration3=0,
#             rain_duration4=0,
#             snow_chance1=0,
#             snow_chance2=0,
#             snow_chance3=0,
#             snow_chance4=0,
#             snow_duration1=0,
#             snow_duration2=0,
#             snow_duration3=0,
#             snow_duration4=0,
#             type=0,
#             skylock=0,
#             skip_los=0,
#             music=0,
#             random_loc=3,
#             dragaggro=0,
#             never_idle=0,
#             castdungeon=0,
#             pull_limit=80,
#             graveyard_time=1,
#             max_z=10000,
#             min_expansion=-1,
#             max_expansion=-1,
#             content_flags="",
#             content_flags_disabled="",
#         )

#     def test_short_name_label(self):
#         eqzone = Zone.objects.get(id=1)
#         field_label = eqzone._meta.get_field("short_name").verbose_name
#         self.assertEqual(field_label, "short name")

#     def test_short_name_max_length(self):
#         eqzone = Zone.objects.get(id=1)
#         max_length = eqzone._meta.get_field("short_name").max_length
#         self.assertEqual(max_length, 32)

#     def test_long_name_label(self):
#         eqzone = Zone.objects.get(id=1)
#         field_label = eqzone._meta.get_field("long_name").verbose_name
#         self.assertEqual(field_label, "long name")

#     def test_file_name_label(self):
#         eqzone = Zone.objects.get(id=1)
#         field_label = eqzone._meta.get_field("file_name").verbose_name
#         self.assertEqual(field_label, "file name")

#     def test_file_name_max_length(self):
#         eqzone = Zone.objects.get(id=1)
#         max_length = eqzone._meta.get_field("file_name").max_length
#         self.assertEqual(max_length, 16)

# class RaceModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         Race.objects.create(name='Test Race', id=1, no_coin=False)

#     def test_name_label(self):
#         eqrace = Race.objects.get(id=1)
#         field_label = eqrace._meta.get_field('name').verbose_name
#         self.assertEqual(field_label, 'name')

#     def test_name_max_length(self):
#         eqrace = Race.objects.get(id=1)
#         max_length = eqrace._meta.get_field('name').max_length
#         self.assertEqual(max_length, 64)

#     def test_no_coin_label(self):
#         eqrace = Race.objects.get(id=1)
#         field_label = eqrace._meta.get_field('no_coin').verbose_name
#         self.assertEqual(field_label, 'no coin')


# class NpcTypeModelTest(TestCase):
#     def test_create_and_retrieve_eq_npc_types(self):
        
#         npc = NpcType.objects.create(
#             name="Test NPC",
#             level=1,
#             race=1,
#             class_field=1,
#             hp=100,
#             mana=100,
#             gender=0,
#             size=1.0,
#             STR=75,
#             STA=75,
#             DEX=75,
#             AGI=75,
#             _INT=80,
#             WIS=75,
#             CHA=75,
#             ATK=0,
#             Accuracy=0,
#             maxlevel=1,
#             scalerate=100,
#             spellscale=100,
#             healscale=100,
#             light=0,
#             walkspeed=0.0,
#             combat_hp_regen=0,
#             combat_mana_regen=0,
#             aggro_pc=0,
#             ignore_distance=600,
#             encounter=0,
#             avoidance=0,
#             exp_pct=100,
#             greed=0,
#             engage_notice=0,
#             stuck_behavior=0,
#             flymode=-1,
#             skip_global_loot=0,
#             rare_spawn=0
#         )

#         same_npc = NpcType.objects.get(id=npc.id)

#         self.assertEqual(same_npc.name, "Test NPC")
#         self.assertEqual(same_npc.level, 1)
#         self.assertEqual(same_npc.race, 1)
#         self.assertEqual(same_npc.class_field, 1)
#         self.assertEqual(same_npc.hp, 100)
#         self.assertEqual(same_npc.mana, 100)
#         self.assertEqual(same_npc.gender, 0)
#         self.assertEqual(same_npc.size, 1.0)
#         self.assertEqual(same_npc.STR, 75)
#         self.assertEqual(same_npc.STA, 75)
#         self.assertEqual(same_npc.DEX, 75)
#         self.assertEqual(same_npc.AGI, 75)
#         self.assertEqual(same_npc._INT, 80)
#         self.assertEqual(same_npc.WIS, 75)
#         self.assertEqual(same_npc.CHA, 75)
#         self.assertEqual(same_npc.ATK, 0)
#         self.assertEqual(same_npc.Accuracy, 0)
#         self.assertEqual(same_npc.maxlevel, 1)
#         self.assertEqual(same_npc.scalerate, 100)
#         self.assertEqual(same_npc.spellscale, 100)
#         self.assertEqual(same_npc.healscale, 100)
#         self.assertEqual(same_npc.light, 0)
#         self.assertEqual(same_npc.walkspeed, 0.0)
#         self.assertEqual(same_npc.combat_hp_regen, 0)
#         self.assertEqual(same_npc.combat_mana_regen, 0)
#         self.assertEqual(same_npc.aggro_pc, 0)
#         self.assertEqual(same_npc.ignore_distance, 600)
#         self.assertEqual(same_npc.encounter, 0)
#         self.assertEqual(same_npc.avoidance, 0)
#         self.assertEqual(same_npc.exp_pct, 100)
#         self.assertEqual(same_npc.greed, 0)
#         self.assertEqual(same_npc.engage_notice, 0)
#         self.assertEqual(same_npc.stuck_behavior, 0)
#         self.assertEqual(same_npc.flymode, -1)
#         self.assertEqual(same_npc.skip_global_loot, 0)
#         self.assertEqual(same_npc.rare_spawn, 0)

        
        