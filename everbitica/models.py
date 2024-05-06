from django.db import models
from django.contrib.auth.models import User


def __str__(self):
    return self.name


class Book(models.Model):
    name = models.CharField(max_length=30, unique=True, default="")
    txtfile = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "eq_books"
        managed = False


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
        managed = False


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
        managed = False


class LootdropEntry(models.Model):
    lootdrop = models.ForeignKey(Lootdrop, on_delete=models.CASCADE)
    item = models.ForeignKey(
        "Item", on_delete=models.CASCADE, db_column="item_id", default=0
    )
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
        managed = False


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
        managed = False


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
        unique_together = (("loottable", "lootdrop"),)  # TODO: needed, maybe bad?
        managed = False


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
    zone_exp_multiplier = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00
    )
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
    flag_needed = models.CharField(max_length=128, default="")
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
            models.Index(
                fields=[
                    "zoneidnumber",
                ]
            ),
            models.Index(
                fields=[
                    "short_name",
                ]
            ),
        ]
        db_table = "eq_zone"
        managed = False


class Race(models.Model):
    name = models.CharField(max_length=64, primary_key=True, default="")
    id = models.IntegerField(default=0)
    no_coin = models.BooleanField(default=False)

    class Meta:
        db_table = "eq_races"
        managed = False


class NpcType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    lastname = models.CharField(max_length=32, null=True, blank=True)
    level = models.PositiveSmallIntegerField(default=0)
    race = models.PositiveSmallIntegerField(default=0)
    class_field = models.PositiveSmallIntegerField(default=0, db_column="class")
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
    _INT = models.PositiveIntegerField(default=80, db_column="_INT")
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
        db_table = "eq_npc_types"
        managed = False


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
        db_table = "eq_spawn2"
        managed = False


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
        db_table = "eq_spawnentry"
        managed = False


class Spawngroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="", unique=True)
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
        db_table = "eq_spawngroup"
        managed = False


class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    minstatus = models.SmallIntegerField()
    name = models.CharField(max_length=64)
    aagi = models.IntegerField()
    ac = models.IntegerField()
    acha = models.IntegerField()
    adex = models.IntegerField()
    aint = models.IntegerField()
    asta = models.IntegerField()
    astr = models.IntegerField()
    awis = models.IntegerField()
    bagsize = models.IntegerField()
    bagslots = models.IntegerField()
    bagtype = models.IntegerField()
    bagwr = models.IntegerField()
    banedmgamt = models.IntegerField()
    banedmgbody = models.IntegerField()
    banedmgrace = models.IntegerField()
    bardtype = models.IntegerField()
    bardvalue = models.IntegerField()
    book = models.IntegerField()
    casttime = models.IntegerField()
    casttime_2 = models.IntegerField()
    classes = models.IntegerField()
    color = models.IntegerField()
    price = models.IntegerField()
    cr = models.IntegerField()
    damage = models.IntegerField()
    deity = models.IntegerField()
    delay = models.IntegerField()
    dr = models.IntegerField()
    clicktype = models.IntegerField()
    clicklevel2 = models.IntegerField()
    elemdmgtype = models.IntegerField()
    elemdmgamt = models.IntegerField()
    factionamt1 = models.IntegerField()
    factionamt2 = models.IntegerField()
    factionamt3 = models.IntegerField()
    factionamt4 = models.IntegerField()
    factionmod1 = models.IntegerField()
    factionmod2 = models.IntegerField()
    factionmod3 = models.IntegerField()
    factionmod4 = models.IntegerField()
    filename = models.CharField(max_length=32)
    focuseffect = models.IntegerField()
    fr = models.IntegerField()
    fvnodrop = models.IntegerField()
    clicklevel = models.IntegerField()
    hp = models.IntegerField()
    icon = models.IntegerField()
    idfile = models.CharField(max_length=30)
    itemclass = models.IntegerField()
    itemtype = models.IntegerField()
    light = models.IntegerField()
    lore = models.CharField(max_length=80)
    magic = models.IntegerField()
    mana = models.IntegerField()
    material = models.IntegerField()
    maxcharges = models.IntegerField()
    mr = models.IntegerField()
    nodrop = models.IntegerField()
    norent = models.IntegerField()
    pr = models.IntegerField()
    procrate = models.IntegerField()
    races = models.IntegerField()
    range = models.IntegerField()
    reclevel = models.IntegerField()
    recskill = models.IntegerField()
    reqlevel = models.IntegerField()
    sellrate = models.FloatField()
    size = models.IntegerField()
    skillmodtype = models.IntegerField()
    skillmodvalue = models.IntegerField()
    slots = models.IntegerField()
    clickeffect = models.IntegerField()
    tradeskills = models.IntegerField()
    weight = models.IntegerField()
    booktype = models.IntegerField()
    recastdelay = models.IntegerField()
    recasttype = models.IntegerField()
    updated = models.DateTimeField()
    comment = models.CharField(max_length=255)
    stacksize = models.IntegerField()
    stackable = models.IntegerField()
    proceffect = models.IntegerField()
    proctype = models.IntegerField()
    proclevel2 = models.IntegerField()
    proclevel = models.IntegerField()
    worneffect = models.IntegerField()
    worntype = models.IntegerField()
    wornlevel2 = models.IntegerField()
    wornlevel = models.IntegerField()
    focustype = models.IntegerField()
    focuslevel2 = models.IntegerField()
    focuslevel = models.IntegerField()
    scrolleffect = models.IntegerField()
    scrolltype = models.IntegerField()
    scrolllevel2 = models.IntegerField()
    scrolllevel = models.IntegerField()
    serialized = models.DateTimeField(null=True)
    verified = models.DateTimeField(null=True)
    serialization = models.TextField(null=True)
    source = models.CharField(max_length=20)
    lorefile = models.CharField(max_length=32)
    questitemflag = models.IntegerField()
    clickunk5 = models.IntegerField()
    clickunk6 = models.CharField(max_length=32)
    clickunk7 = models.IntegerField()
    procunk1 = models.IntegerField()
    procunk2 = models.IntegerField()
    procunk3 = models.IntegerField()
    procunk4 = models.IntegerField()
    procunk6 = models.CharField(max_length=32)
    procunk7 = models.IntegerField()
    wornunk1 = models.IntegerField()
    wornunk2 = models.IntegerField()
    wornunk3 = models.IntegerField()
    wornunk4 = models.IntegerField()
    wornunk5 = models.IntegerField()
    wornunk6 = models.CharField(max_length=32)
    wornunk7 = models.IntegerField()
    focusunk1 = models.IntegerField()
    focusunk2 = models.IntegerField()
    focusunk3 = models.IntegerField()
    focusunk4 = models.IntegerField()
    focusunk5 = models.IntegerField()
    focusunk6 = models.CharField(max_length=32)
    focusunk7 = models.IntegerField()
    scrollunk1 = models.IntegerField()
    scrollunk2 = models.IntegerField()
    scrollunk3 = models.IntegerField()
    scrollunk4 = models.IntegerField()
    scrollunk5 = models.IntegerField()
    scrollunk6 = models.CharField(max_length=32)
    scrollunk7 = models.IntegerField()
    clickname = models.CharField(max_length=64)
    procname = models.CharField(max_length=64)
    wornname = models.CharField(max_length=64)
    focusname = models.CharField(max_length=64)
    scrollname = models.CharField(max_length=64)
    created = models.CharField(max_length=64)
    bardeffect = models.SmallIntegerField()
    bardeffecttype = models.SmallIntegerField()
    bardlevel2 = models.SmallIntegerField()
    bardlevel = models.SmallIntegerField()
    bardunk1 = models.SmallIntegerField()
    bardunk2 = models.SmallIntegerField()
    bardunk3 = models.SmallIntegerField()
    bardunk4 = models.SmallIntegerField()
    bardunk5 = models.SmallIntegerField()
    bardname = models.CharField(max_length=64)
    bardunk7 = models.SmallIntegerField()
    gmflag = models.IntegerField()
    soulbound = models.IntegerField()

    class Meta:
        db_table = "eq_items"
        unique_together = (("id",), ("name",), ("lore",), ("minstatus",))
        managed = False


class CharacterClass(models.Model):
    id = models.IntegerField(primary_key=True)
    bitmask = models.IntegerField(null=True)
    name = models.CharField(max_length=50)
    spell_list_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "eq_classes"


class Spell(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, null=True)
    player_1 = models.CharField(max_length=64, default='BLUE_TRAIL')
    teleport_zone = models.CharField(max_length=64, null=True)
    you_cast = models.CharField(max_length=120, null=True)
    other_casts = models.CharField(max_length=120, null=True)
    cast_on_you = models.CharField(max_length=120, null=True)
    cast_on_other = models.CharField(max_length=120, null=True)
    spell_fades = models.CharField(max_length=120, null=True)
    range = models.IntegerField(default=100)
    aoerange = models.IntegerField(default=0)
    pushback = models.FloatField(default=0.00)
    pushup = models.FloatField(default=0.00)
    cast_time = models.IntegerField(default=0)
    recovery_time = models.IntegerField(default=0)
    recast_time = models.IntegerField(default=0)
    buffdurationformula = models.IntegerField(default=7)
    buffduration = models.IntegerField(default=65)
    AEDuration = models.IntegerField(default=0)
    mana = models.IntegerField(default=0)
    effect_base_value1 = models.IntegerField(default=100)
    effect_base_value2 = models.IntegerField(default=0)
    effect_base_value3 = models.IntegerField(default=0)
    effect_base_value4 = models.IntegerField(default=0)
    effect_base_value5 = models.IntegerField(default=0)
    effect_base_value6 = models.IntegerField(default=0)
    effect_base_value7 = models.IntegerField(default=0)
    effect_base_value8 = models.IntegerField(default=0)
    effect_base_value9 = models.IntegerField(default=0)
    effect_base_value10 = models.IntegerField(default=0)
    effect_base_value11 = models.IntegerField(default=0)
    effect_base_value12 = models.IntegerField(default=0)
    effect_limit_value1 = models.IntegerField(default=0)
    effect_limit_value2 = models.IntegerField(default=0)
    effect_limit_value3 = models.IntegerField(default=0)
    effect_limit_value4 = models.IntegerField(default=0)
    effect_limit_value5 = models.IntegerField(default=0)
    effect_limit_value6 = models.IntegerField(default=0)
    effect_limit_value7 = models.IntegerField(default=0)
    effect_limit_value8 = models.IntegerField(default=0)
    effect_limit_value9 = models.IntegerField(default=0)
    effect_limit_value10 = models.IntegerField(default=0)
    effect_limit_value11 = models.IntegerField(default=0)
    effect_limit_value12 = models.IntegerField(default=0)
    max1 = models.IntegerField(default=0)
    max2 = models.IntegerField(default=0)
    max3 = models.IntegerField(default=0)
    max4 = models.IntegerField(default=0)
    max5 = models.IntegerField(default=0)
    max6 = models.IntegerField(default=0)
    max7 = models.IntegerField(default=0)
    max8 = models.IntegerField(default=0)
    max9 = models.IntegerField(default=0)
    max10 = models.IntegerField(default=0)
    max11 = models.IntegerField(default=0)
    max12 = models.IntegerField(default=0)
    icon = models.IntegerField(default=0)
    memicon = models.IntegerField(default=0)
    components1 = models.IntegerField(default=-1)
    components2 = models.IntegerField(default=-1)
    components3 = models.IntegerField(default=-1)
    components4 = models.IntegerField(default=-1)
    component_counts1 = models.IntegerField(default=1)
    component_counts2 = models.IntegerField(default=1)
    component_counts3 = models.IntegerField(default=1)
    component_counts4 = models.IntegerField(default=1)
    NoexpendReagent1 = models.IntegerField(default=-1)
    NoexpendReagent2 = models.IntegerField(default=-1)
    NoexpendReagent3 = models.IntegerField(default=-1)
    NoexpendReagent4 = models.IntegerField(default=-1)
    formula1 = models.IntegerField(default=100)
    formula2 = models.IntegerField(default=100)
    formula3 = models.IntegerField(default=100)
    formula4 = models.IntegerField(default=100)
    formula5 = models.IntegerField(default=100)
    formula6 = models.IntegerField(default=100)
    formula7 = models.IntegerField(default=100)
    formula8 = models.IntegerField(default=100)
    formula9 = models.IntegerField(default=100)
    formula10 = models.IntegerField(default=100)
    formula11 = models.IntegerField(default=100)
    formula12 = models.IntegerField(default=100)
    LightType = models.IntegerField(default=0)
    goodEffect = models.IntegerField(default=0)
    Activated = models.IntegerField(default=0)
    resisttype = models.IntegerField(default=0)
    effectid1 = models.IntegerField(default=254)
    effectid2 = models.IntegerField(default=254)
    effectid3 = models.IntegerField(default=254)
    effectid4 = models.IntegerField(default=254)
    effectid5 = models.IntegerField(default=254)
    effectid6 = models.IntegerField(default=254)
    effectid7 = models.IntegerField(default=254)
    effectid8 = models.IntegerField(default=254)
    effectid9 = models.IntegerField(default=254)
    effectid10 = models.IntegerField(default=254)
    effectid11 = models.IntegerField(default=254)
    effectid12 = models.IntegerField(default=254)
    targettype = models.IntegerField(default=2)
    basediff = models.IntegerField(default=0)
    skill = models.IntegerField(default=98)
    zonetype = models.IntegerField(default=-1)
    EnvironmentType = models.IntegerField(default=0)
    TimeOfDay = models.IntegerField(default=0)
    classes1 = models.IntegerField(default=255)
    classes2 = models.IntegerField(default=255)
    classes3 = models.IntegerField(default=255)
    classes4 = models.IntegerField(default=255)
    classes5 = models.IntegerField(default=255)
    classes6 = models.IntegerField(default=255)
    classes7 = models.IntegerField(default=255)
    classes8 = models.IntegerField(default=255)
    classes9 = models.IntegerField(default=255)
    classes10 = models.IntegerField(default=255)
    classes11 = models.IntegerField(default=255)
    classes12 = models.IntegerField(default=255)
    classes13 = models.IntegerField(default=255)
    classes14 = models.IntegerField(default=255)
    classes15 = models.IntegerField(default=255)
    CastingAnim = models.IntegerField(default=44)
    TargetAnim = models.IntegerField(default=13)
    TravelType = models.IntegerField(default=0)
    SpellAffectIndex = models.IntegerField(default=-1)
    disallow_sit = models.IntegerField(default=0)
    deities0 = models.IntegerField(default=0)
    deities1 = models.IntegerField(default=0)
    deities2 = models.IntegerField(default=0)
    deities3 = models.IntegerField(default=0)
    deities4 = models.IntegerField(default=0)
    deities5 = models.IntegerField(default=0)
    deities6 = models.IntegerField(default=0)
    deities7 = models.IntegerField(default=0)
    deities8 = models.IntegerField(default=0)
    deities9 = models.IntegerField(default=0)
    deities10 = models.IntegerField(default=0)
    deities11 = models.IntegerField(default=0)
    deities12 = models.IntegerField(default=0)
    deities13 = models.IntegerField(default=0)
    deities14 = models.IntegerField(default=0)
    deities15 = models.IntegerField(default=0)
    deities16 = models.IntegerField(default=0)
    npc_no_cast = models.IntegerField(default=0)
    ai_pt_bonus = models.IntegerField(default=0)
    new_icon = models.IntegerField(default=161)
    spellanim = models.IntegerField(default=0)
    uninterruptable = models.IntegerField(default=0)
    ResistDiff = models.IntegerField(default=-150)
    dot_stacking_exempt = models.IntegerField(default=0)
    deleteable = models.IntegerField(default=0)
    RecourseLink = models.IntegerField(default=0)
    no_partial_resist = models.IntegerField(default=0)
    small_targets_only = models.IntegerField(default=0)
    use_persistent_particles = models.IntegerField(default=0)
    short_buff_box = models.IntegerField(default=-1)
    descnum = models.IntegerField(default=0)
    typedescnum = models.IntegerField(null=True)
    effectdescnum = models.IntegerField(null=True)
    effectdescnum2 = models.IntegerField(default=0)
    npc_no_los = models.IntegerField(default=0)
    reflectable = models.IntegerField(default=0)
    resist_per_level = models.IntegerField(default=0)
    resist_cap = models.IntegerField(default=0)
    EndurCost = models.IntegerField(default=0)
    EndurTimerIndex = models.IntegerField(default=0)
    IsDiscipline = models.IntegerField(default=0)
    HateAdded = models.IntegerField(default=0)
    EndurUpkeep = models.IntegerField(default=0)
    pvpresistbase = models.IntegerField(default=-150)
    pvpresistcalc = models.IntegerField(default=100)
    pvpresistcap = models.IntegerField(default=-150)
    spell_category = models.IntegerField(default=-99)
    pvp_duration = models.IntegerField(default=0)
    pvp_duration_cap = models.IntegerField(default=0)
    cast_not_standing = models.IntegerField(default=0)
    can_mgb = models.IntegerField(default=0)
    nodispell = models.IntegerField(default=-1)
    npc_category = models.IntegerField(default=0)
    npc_usefulness = models.IntegerField(default=0)
    wear_off_message = models.IntegerField(default=0)
    suspendable = models.IntegerField(default=0)
    spellgroup = models.IntegerField(default=0)
    allow_spellscribe = models.IntegerField(default=0)
    allowrest = models.IntegerField(default=0)
    custom_icon = models.IntegerField(default=0)
    not_player_spell = models.IntegerField(default=0)
    disabled = models.IntegerField(default=0)

    class Meta:
        db_table = "eq_spells_new"
        managed = False

class Deity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "eq_deities"

class CharacterData(models.Model):
    id = models.AutoField(primary_key=True)
    account_id = models.IntegerField(default=0)
    forum_id = models.IntegerField(default=0)
    name = models.CharField(max_length=64, unique=True)
    last_name = models.CharField(max_length=64, default='')
    title = models.CharField(max_length=32, default='')
    suffix = models.CharField(max_length=32, default='')
    zone_id = models.IntegerField(default=0)
    y = models.FloatField(default=0)
    x = models.FloatField(default=0)
    z = models.FloatField(default=0)
    heading = models.FloatField(default=0)
    gender = models.PositiveSmallIntegerField(default=0)
    race = models.PositiveSmallIntegerField(default=0)
    class_field = models.PositiveSmallIntegerField(default=0, db_column='class')
    level = models.PositiveIntegerField(default=0)
    deity = models.PositiveIntegerField(default=0)
    birthday = models.PositiveIntegerField(default=0)
    last_login = models.PositiveIntegerField(default=0)
    time_played = models.PositiveIntegerField(default=0)
    level2 = models.PositiveSmallIntegerField(default=0)
    anon = models.PositiveSmallIntegerField(default=0)
    gm = models.PositiveSmallIntegerField(default=0)
    face = models.PositiveIntegerField(default=0)
    hair_color = models.PositiveSmallIntegerField(default=0)
    hair_style = models.PositiveSmallIntegerField(default=0)
    beard = models.PositiveSmallIntegerField(default=0)
    beard_color = models.PositiveSmallIntegerField(default=0)
    eye_color_1 = models.PositiveSmallIntegerField(default=0)
    eye_color_2 = models.PositiveSmallIntegerField(default=0)
    exp = models.PositiveIntegerField(default=0)
    aa_points_spent = models.PositiveIntegerField(default=0)
    aa_exp = models.PositiveIntegerField(default=0)
    aa_points = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    cur_hp = models.PositiveIntegerField(default=0)
    mana = models.PositiveIntegerField(default=0)
    endurance = models.PositiveIntegerField(default=0)
    intoxication = models.PositiveIntegerField(default=0)
    str = models.PositiveIntegerField(default=0)
    sta = models.PositiveIntegerField(default=0)
    cha = models.PositiveIntegerField(default=0)
    dex = models.PositiveIntegerField(default=0)
    int = models.PositiveIntegerField(default=0, db_column='int')
    agi = models.PositiveIntegerField(default=0)
    wis = models.PositiveIntegerField(default=0)
    zone_change_count = models.PositiveIntegerField(default=0)
    hunger_level = models.PositiveIntegerField(default=0)
    thirst_level = models.PositiveIntegerField(default=0)
    pvp_status = models.PositiveSmallIntegerField(default=0)
    air_remaining = models.PositiveIntegerField(default=0)
    autosplit_enabled = models.PositiveIntegerField(default=0)
    mailkey = models.CharField(max_length=16, default='')
    firstlogon = models.PositiveSmallIntegerField(default=0)
    e_aa_effects = models.PositiveIntegerField(default=0)
    e_percent_to_aa = models.PositiveIntegerField(default=0)
    e_expended_aa_spent = models.PositiveIntegerField(default=0)
    boatid = models.PositiveIntegerField(default=0)
    boatname = models.CharField(max_length=25, null=True)
    famished = models.IntegerField(default=0)
    is_deleted = models.PositiveSmallIntegerField(default=0)
    showhelm = models.PositiveSmallIntegerField(default=1)
    fatigue = models.IntegerField(default=0)

    class Meta:
        db_table = "eq_character_data"


class CharacterCurrency(models.Model):
    id = models.AutoField(primary_key=True)
    character_data = models.OneToOneField(CharacterData, on_delete=models.CASCADE)
    platinum = models.PositiveIntegerField(default=0)
    gold = models.PositiveIntegerField(default=0)
    silver = models.PositiveIntegerField(default=0)
    copper = models.PositiveIntegerField(default=0)
    platinum_bank = models.PositiveIntegerField(default=0)
    gold_bank = models.PositiveIntegerField(default=0)
    silver_bank = models.PositiveIntegerField(default=0)
    copper_bank = models.PositiveIntegerField(default=0)
    platinum_cursor = models.PositiveIntegerField(default=0)
    gold_cursor = models.PositiveIntegerField(default=0)
    silver_cursor = models.PositiveIntegerField(default=0)
    copper_cursor = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "eq_character_currency"


class CharacterFactionValues(models.Model):
    id = models.AutoField(primary_key=True)
    faction_id = models.PositiveSmallIntegerField(default=0)
    current_value = models.SmallIntegerField(default=0)
    temp = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "eq_character_faction_values"
        unique_together = (("id", "faction_id"),)


class CharacterInventory(models.Model):
    id = models.AutoField(primary_key=True)
    character_data = models.ForeignKey('CharacterData', on_delete=models.CASCADE)
    slotid = models.PositiveIntegerField(default=0)
    itemid = models.PositiveIntegerField(default=0, null=True)
    charges = models.PositiveSmallIntegerField(default=0)
    custom_data = models.TextField(null=True)
    serialnumber = models.PositiveIntegerField(default=0)
    initialserial = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "eq_character_inventory"
        unique_together = (("id", "slotid"),)


class CharacterSkills(models.Model):
    id = models.AutoField(primary_key=True)
    skill_id = models.PositiveSmallIntegerField(default=0)
    value = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "eq_character_skills"
        unique_together = (("id", "skill_id"),)

class CharacterSpells(models.Model):
    id = models.AutoField(primary_key=True)
    slot_id = models.PositiveSmallIntegerField(default=0)
    spell_id = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "eq_character_spells"
        unique_together = (("id", "slot_id"),)

class CharacterMemmedSpells(models.Model):
    id = models.AutoField(primary_key=True)
    slot_id = models.PositiveSmallIntegerField(default=0)
    spell_id = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "eq_character_memmed_spells"
        unique_together = (("id", "slot_id"),)


class CharacterBuffs(models.Model):
    id = models.AutoField(primary_key=True)
    slot_id = models.PositiveSmallIntegerField()
    spell_id = models.PositiveSmallIntegerField()
    caster_level = models.PositiveSmallIntegerField()
    caster_name = models.CharField(max_length=64)
    ticsremaining = models.PositiveIntegerField()
    counters = models.PositiveIntegerField()
    melee_rune = models.PositiveIntegerField()
    magic_rune = models.PositiveIntegerField()
    persistent = models.PositiveSmallIntegerField()
    ExtraDIChance = models.IntegerField(default=0)
    bard_modifier = models.PositiveSmallIntegerField(default=10)
    bufftype = models.IntegerField()

    class Meta:
        db_table = "eq_character_buffs"
        unique_together = (("id", "slot_id"),)


class MerchantInventory(models.Model):
    id = models.AutoField(primary_key=True)
    npcid = models.PositiveIntegerField(default=0)
    slot = models.PositiveSmallIntegerField(default=0)
    itemid = models.PositiveIntegerField(default=0)
    charges = models.PositiveIntegerField(default=1)
    quantity = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "eq_merchant_inventory"
        unique_together = (("npcid", "slot"),)