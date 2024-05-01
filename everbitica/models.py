from django.db import models
from django.contrib.auth.models import User


def __str__(self):
    return self.name


class PlayerClass(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_playable = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ArmorType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=30, unique=True, default="")
    txtfile = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "eq_books"


class Faction(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    base = models.SmallIntegerField(default=0)
    see_illusion = models.BooleanField(default=True)
    min_cap = models.SmallIntegerField(default=0)
    max_cap = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "eq_faction_list"


"""
Looting system breakdown:

TLDR: NPCs have a loottable ID, loottables have lootdrops, lootdrops have items.

NPCs: These are the characters in the game that aren't controlled by players. Each NPC has a loottable_id which determines what items they can drop when defeated.

eq_loottable: This table is like a list of possible sets of items that an NPC can drop. Each row represents a different set, identified by a unique id. An NPC is linked to one of these sets (or 'loot tables') via its loottable_id.

eq_loottable_entries: This table links the loot tables to the actual items. Each row represents a possible item that can be dropped from a loot table. It does this by having a loottable_id (linking it to a row in eq_loottable) and a lootdrop_id (linking it to a row in eq_lootdrop).

eq_lootdrop: This table represents a collection of items that can be dropped together. Each row is a different collection, identified by a unique id.

eq_lootdrop_entries: This table links the loot drops to the actual items. Each row represents an item that can be part of a loot drop. It does this by having a lootdrop_id (linking it to a row in eq_lootdrop) and an item_id (presumably linking it to a specific item).

So, to find out what items an NPC can drop, you would:

1. Look at the NPC's loottable_id.
2. Find all rows in eq_loottable_entries with that loottable_id.
3. For each of those rows, look at the lootdrop_id.
4. Find all rows in eq_lootdrop_entries with that lootdrop_id.
5. For each of those rows, look at the item_id to find the actual item.

This structure allows for a lot of flexibility. For example, multiple NPCs can share the same loot table, meaning they drop the same sets of items. Similarly, multiple loot tables can include the same loot drop, meaning they can drop the same collections of items.

Example SQL query:

SELECT items.* FROM items INNER JOIN lootdrop_entries ON items.id = lootdrop_entries.item_id INNER JOIN loottable_entries ON lootdrop_entries.lootdrop_id = loottable_entries.lootdrop_id INNER JOIN npc_types ON loottable_entries.loottable_id = npc_types.loottable_id WHERE npc_types.id = #;
"""


class Lootdrop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default="")
    min_expansion = models.SmallIntegerField(default=-1)
    max_expansion = models.SmallIntegerField(default=-1)
    content_flags = models.CharField(max_length=100, null=True)
    content_flags_disabled = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "eq_lootdrop"


class LootdropEntry(models.Model):
    lootdrop = models.ForeignKey(Lootdrop, on_delete=models.CASCADE)
    item_id = models.IntegerField()
    item_charges = models.SmallIntegerField(default=1)
    equip_item = models.SmallIntegerField(default=0)
    chance = models.FloatField(default=1)
    minlevel = models.SmallIntegerField(default=0)
    maxlevel = models.SmallIntegerField(default=255)
    multiplier = models.SmallIntegerField(default=1)
    disabled_chance = models.FloatField(default=0)

    class Meta:
        db_table = "eq_lootdrop_entries"
        unique_together = (("lootdrop", "item_id"),)


class Loottable(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default="")
    mincash = models.IntegerField(default=0)
    maxcash = models.IntegerField(default=0)
    avgcoin = models.IntegerField(default=0)
    done = models.SmallIntegerField(default=0)
    min_expansion = models.SmallIntegerField(default=-1)
    max_expansion = models.SmallIntegerField(default=-1)
    content_flags = models.CharField(max_length=100, null=True)
    content_flags_disabled = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "eq_loottable"


class LoottableEntry(models.Model):
    loottable = models.ForeignKey(Loottable, on_delete=models.CASCADE)
    lootdrop = models.ForeignKey(Lootdrop, on_delete=models.CASCADE)
    multiplier = models.SmallIntegerField(default=1)
    probability = models.SmallIntegerField(default=100)
    droplimit = models.SmallIntegerField(default=0)
    mindrop = models.SmallIntegerField(default=0)
    multiplier_min = models.SmallIntegerField(default=0)

    class Meta:
        db_table = "eq_loottable_entries"
        unique_together = (("loottable", "lootdrop"),)


class Zone(models.Model):
    short_name = models.CharField(max_length=32, null=True, blank=True)
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=16, null=True, blank=True)
    long_name = models.TextField()
    map_file_name = models.CharField(max_length=100, null=True, blank=True)
    safe_x = models.FloatField(default=0)
    safe_y = models.FloatField(default=0)
    safe_z = models.FloatField(default=0)
    safe_heading = models.FloatField(default=0)
    graveyard_id = models.FloatField(default=0)
    min_level = models.PositiveSmallIntegerField(default=0)
    min_status = models.PositiveSmallIntegerField(default=0)
    zoneidnumber = models.IntegerField(default=0)
    timezone = models.IntegerField(default=0)
    maxclients = models.IntegerField(default=0)
    ruleset = models.PositiveIntegerField(default=0)
    note = models.CharField(max_length=80, null=True, blank=True)
    underworld = models.FloatField(default=0)
    minclip = models.FloatField(default=450)
    maxclip = models.FloatField(default=450)
    fog_minclip = models.FloatField(default=450)
    fog_maxclip = models.FloatField(default=450)
    fog_blue = models.PositiveSmallIntegerField(default=0)
    fog_red = models.PositiveSmallIntegerField(default=0)
    fog_green = models.PositiveSmallIntegerField(default=0)
    sky = models.PositiveSmallIntegerField(default=1)
    ztype = models.PositiveSmallIntegerField(default=1)
    zone_exp_multiplier = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    gravity = models.FloatField(default=0.4)
    time_type = models.PositiveSmallIntegerField(default=2)
    fog_red1 = models.PositiveSmallIntegerField(default=0)
    fog_green1 = models.PositiveSmallIntegerField(default=0)
    fog_blue1 = models.PositiveSmallIntegerField(default=0)
    fog_minclip1 = models.FloatField(default=450)
    fog_maxclip1 = models.FloatField(default=450)
    fog_red2 = models.PositiveSmallIntegerField(default=0)
    fog_green2 = models.PositiveSmallIntegerField(default=0)
    fog_blue2 = models.PositiveSmallIntegerField(default=0)
    fog_minclip2 = models.FloatField(default=450)
    fog_maxclip2 = models.FloatField(default=450)
    fog_red3 = models.PositiveSmallIntegerField(default=0)
    fog_green3 = models.PositiveSmallIntegerField(default=0)
    fog_blue3 = models.PositiveSmallIntegerField(default=0)
    fog_minclip3 = models.FloatField(default=450)
    fog_maxclip3 = models.FloatField(default=450)
    fog_red4 = models.PositiveSmallIntegerField(default=0)
    fog_green4 = models.PositiveSmallIntegerField(default=0)
    fog_blue4 = models.PositiveSmallIntegerField(default=0)
    fog_minclip4 = models.FloatField(default=450)
    fog_maxclip4 = models.FloatField(default=450)
    fog_density = models.FloatField(default=0)
    flag_needed = models.CharField(max_length=128, default='')
    canbind = models.SmallIntegerField(default=1)
    cancombat = models.SmallIntegerField(default=1)
    canlevitate = models.SmallIntegerField(default=1)
    castoutdoor = models.SmallIntegerField(default=1)
    hotzone = models.PositiveSmallIntegerField(default=0)
    shutdowndelay = models.PositiveBigIntegerField(default=5000)
    peqzone = models.SmallIntegerField(default=1)
    expansion = models.PositiveSmallIntegerField(default=0)
    suspendbuffs = models.PositiveSmallIntegerField(default=0)
    rain_chance1 = models.IntegerField(default=0)
    rain_chance2 = models.IntegerField(default=0)
    rain_chance3 = models.IntegerField(default=0)
    rain_chance4 = models.IntegerField(default=0)
    rain_duration1 = models.IntegerField(default=0)
    rain_duration2 = models.IntegerField(default=0)
    rain_duration3 = models.IntegerField(default=0)
    rain_duration4 = models.IntegerField(default=0)
    snow_chance1 = models.IntegerField(default=0)
    snow_chance2 = models.IntegerField(default=0)
    snow_chance3 = models.IntegerField(default=0)
    snow_chance4 = models.IntegerField(default=0)
    snow_duration1 = models.IntegerField(default=0)
    snow_duration2 = models.IntegerField(default=0)
    snow_duration3 = models.IntegerField(default=0)
    snow_duration4 = models.IntegerField(default=0)
    type = models.IntegerField(default=0)
    skylock = models.SmallIntegerField(default=0)
    skip_los = models.SmallIntegerField(default=0)
    music = models.SmallIntegerField(default=0)
    random_loc = models.PositiveSmallIntegerField(default=3)
    dragaggro = models.PositiveSmallIntegerField(default=0)
    never_idle = models.PositiveSmallIntegerField(default=0)
    castdungeon = models.SmallIntegerField(default=0)
    pull_limit = models.PositiveSmallIntegerField(default=80)
    graveyard_time = models.IntegerField(default=1)
    max_z = models.FloatField(default=10000)
    min_expansion = models.SmallIntegerField(default=-1)
    max_expansion = models.SmallIntegerField(default=-1)
    content_flags = models.CharField(max_length=100, null=True, blank=True)
    content_flags_disabled = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['zoneidnumber',]),
            models.Index(fields=['short_name',]),
        ]


class Race(models.Model):
    name = models.CharField(max_length=64, primary_key=True, default='')
    id = models.IntegerField(default=0)
    no_coin = models.BooleanField(default=False)

    class Meta:
        db_table = 'eq_races'



class NpcType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    lastname = models.CharField(max_length=32, null=True, blank=True)
    level = models.PositiveSmallIntegerField(default=0)
    race = models.PositiveSmallIntegerField(default=0)
    class_field = models.PositiveSmallIntegerField(default=0, db_column='class')
    bodytype = models.IntegerField(default=1)
    hp = models.IntegerField(default=0)
    mana = models.IntegerField(default=0)
    gender = models.PositiveSmallIntegerField(default=0)
    texture = models.PositiveSmallIntegerField(default=0)
    helmtexture = models.PositiveSmallIntegerField(default=0)
    size = models.FloatField(default=0)
    hp_regen_rate = models.PositiveIntegerField(default=0)
    mana_regen_rate = models.PositiveIntegerField(default=0)
    loottable_id = models.PositiveIntegerField(default=0)
    merchant_id = models.PositiveIntegerField(default=0)
    npc_spells_id = models.PositiveIntegerField(default=0)
    npc_spells_effects_id = models.PositiveIntegerField(default=0)
    npc_faction_id = models.IntegerField(default=0)
    mindmg = models.PositiveIntegerField(default=0)
    maxdmg = models.PositiveIntegerField(default=0)
    attack_count = models.SmallIntegerField(default=-1)
    special_abilities = models.TextField(null=True, blank=True)
    aggroradius = models.PositiveIntegerField(default=0)
    assistradius = models.PositiveIntegerField(default=0)
    face = models.PositiveIntegerField(default=1)
    luclin_hairstyle = models.PositiveIntegerField(default=1)
    luclin_haircolor = models.PositiveIntegerField(default=1)
    luclin_eyecolor = models.PositiveIntegerField(default=1)
    luclin_eyecolor2 = models.PositiveIntegerField(default=1)
    luclin_beardcolor = models.PositiveIntegerField(default=1)
    luclin_beard = models.PositiveIntegerField(default=0)
    armortint_id = models.PositiveIntegerField(default=0)
    armortint_red = models.PositiveSmallIntegerField(default=0)
    armortint_green = models.PositiveSmallIntegerField(default=0)
    armortint_blue = models.PositiveSmallIntegerField(default=0)
    d_melee_texture1 = models.IntegerField(default=0)
    d_melee_texture2 = models.IntegerField(default=0)
    prim_melee_type = models.PositiveSmallIntegerField(default=28)
    sec_melee_type = models.PositiveSmallIntegerField(default=28)
    ranged_type = models.PositiveSmallIntegerField(default=7)
    runspeed = models.FloatField(default=0)
    MR = models.SmallIntegerField(default=0)
    CR = models.SmallIntegerField(default=0)
    DR = models.SmallIntegerField(default=0)
    FR = models.SmallIntegerField(default=0)
    PR = models.SmallIntegerField(default=0)
    see_invis = models.SmallIntegerField(default=0)
    see_invis_undead = models.SmallIntegerField(default=0)
    qglobal = models.PositiveSmallIntegerField(default=0)
    AC = models.SmallIntegerField(default=0)
    npc_aggro = models.PositiveSmallIntegerField(default=0)
    spawn_limit = models.PositiveSmallIntegerField(default=0)
    attack_delay = models.PositiveSmallIntegerField(default=30)
    STR = models.PositiveIntegerField(default=75)
    STA = models.PositiveIntegerField(default=75)
    DEX = models.PositiveIntegerField(default=75)
    AGI = models.PositiveIntegerField(default=75)
    _INT = models.PositiveIntegerField(default=80, db_column='_INT')
    WIS = models.PositiveIntegerField(default=75)
    CHA = models.PositiveIntegerField(default=75)
    see_sneak = models.PositiveSmallIntegerField(default=0)
    see_improved_hide = models.PositiveSmallIntegerField(default=0)
    ATK = models.PositiveIntegerField(default=0)
    Accuracy = models.PositiveIntegerField(default=0)
    slow_mitigation = models.SmallIntegerField(default=0)
    maxlevel = models.PositiveSmallIntegerField(default=0)
    scalerate = models.IntegerField(default=100)
    private_corpse = models.PositiveSmallIntegerField(default=0)
    unique_spawn_by_name = models.PositiveSmallIntegerField(default=0)
    underwater = models.PositiveSmallIntegerField(default=0)
    isquest = models.PositiveSmallIntegerField(default=0)
    emoteid = models.PositiveIntegerField(default=0)
    spellscale = models.FloatField(default=100)
    healscale = models.FloatField(default=100)
    raid_target = models.PositiveSmallIntegerField(default=0)
    chesttexture = models.PositiveSmallIntegerField(default=0)
    armtexture = models.PositiveSmallIntegerField(default=0)
    bracertexture = models.PositiveSmallIntegerField(default=0)
    handtexture = models.PositiveSmallIntegerField(default=0)
    legtexture = models.PositiveSmallIntegerField(default=0)
    feettexture = models.PositiveSmallIntegerField(default=0)
    light = models.PositiveSmallIntegerField(default=0)
    walkspeed = models.FloatField(default=0)
    combat_hp_regen = models.IntegerField(default=0)
    combat_mana_regen = models.IntegerField(default=0)
    aggro_pc = models.PositiveSmallIntegerField(default=0)
    ignore_distance = models.FloatField(default=600)
    encounter = models.PositiveSmallIntegerField(default=0)
    ignore_despawn = models.PositiveSmallIntegerField(default=0)
    avoidance = models.SmallIntegerField(default=0)
    exp_pct = models.PositiveSmallIntegerField(default=100)
    greed = models.PositiveSmallIntegerField(default=0)
    engage_notice = models.PositiveSmallIntegerField(default=0)
    stuck_behavior = models.PositiveSmallIntegerField(default=0)
    flymode = models.SmallIntegerField(default=-1)
    skip_global_loot = models.PositiveSmallIntegerField(default=0)
    rare_spawn = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'eq_npc_types'



class Spawn(models.Model):
    id = models.AutoField(primary_key=True)
    spawngroupID = models.IntegerField(default=0)
    zone = models.CharField(max_length=32, null=True, blank=True)
    x = models.FloatField(default=0.0)
    y = models.FloatField(default=0.0)
    z = models.FloatField(default=0.0)
    heading = models.FloatField(default=0.0)
    respawntime = models.IntegerField(default=0)
    variance = models.IntegerField(default=0)
    pathgrid = models.IntegerField(default=0)
    _condition = models.PositiveIntegerField(default=0)
    cond_value = models.IntegerField(default=1)
    enabled = models.PositiveSmallIntegerField(default=1)
    animation = models.PositiveSmallIntegerField(default=0)
    boot_respawntime = models.IntegerField(default=0)
    clear_timer_onboot = models.PositiveSmallIntegerField(default=0)
    boot_variance = models.IntegerField(default=0)
    force_z = models.PositiveSmallIntegerField(default=0)
    min_expansion = models.SmallIntegerField(default=-1)
    max_expansion = models.SmallIntegerField(default=-1)
    content_flags = models.CharField(max_length=100, null=True, blank=True)
    content_flags_disabled = models.CharField(max_length=100, null=True, blank=True)


    class Meta:
        db_table = 'eq_spawn2'

class Spawnentry(models.Model):
    spawngroupID = models.IntegerField(default=0, primary_key=True)
    npcID = models.IntegerField(default=0)
    chance = models.SmallIntegerField(default=0)
    mintime = models.SmallIntegerField(default=0)
    maxtime = models.SmallIntegerField(default=0)
    min_expansion = models.SmallIntegerField(default=-1)
    max_expansion = models.SmallIntegerField(default=-1)
    content_flags = models.CharField(max_length=100, null=True, blank=True)
    content_flags_disabled = models.CharField(max_length=100, null=True, blank=True)


    class Meta:
        db_table = 'eq_spawnentry'

class Spawngroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='', unique=True)
    spawn_limit = models.SmallIntegerField(default=0)
    max_x = models.FloatField(default=0.0)
    min_x = models.FloatField(default=0.0)
    max_y = models.FloatField(default=0.0)
    min_y = models.FloatField(default=0.0)
    delay = models.IntegerField(default=45000)
    mindelay = models.IntegerField(default=15000)
    despawn = models.PositiveSmallIntegerField(default=0)
    despawn_timer = models.IntegerField(default=100)
    rand_spawns = models.IntegerField(default=0)
    rand_respawntime = models.IntegerField(default=1200)
    rand_variance = models.IntegerField(default=0)
    rand_condition = models.IntegerField(default=0)
    wp_spawns = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'eq_spawngroup'