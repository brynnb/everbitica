from django.db import models
from django.contrib.auth.models import User


# Create your models here.
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


class Books(models.Model):
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

class Lootdrop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default='')
    min_expansion = models.SmallIntegerField(default=-1)
    max_expansion = models.SmallIntegerField(default=-1)
    content_flags = models.CharField(max_length=100, null=True)
    content_flags_disabled = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'eq_lootdrop'


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
        db_table = 'eq_lootdrop_entries'
        unique_together = (('lootdrop', 'item_id'),)


class Loottable(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, default='')
    mincash = models.IntegerField(default=0)
    maxcash = models.IntegerField(default=0)
    avgcoin = models.IntegerField(default=0)
    done = models.SmallIntegerField(default=0)
    min_expansion = models.SmallIntegerField(default=-1)
    max_expansion = models.SmallIntegerField(default=-1)
    content_flags = models.CharField(max_length=100, null=True)
    content_flags_disabled = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'eq_loottable'


class LoottableEntry(models.Model):
    loottable = models.ForeignKey(Loottable, on_delete=models.CASCADE)
    lootdrop = models.ForeignKey(Lootdrop, on_delete=models.CASCADE)
    multiplier = models.SmallIntegerField(default=1)
    probability = models.SmallIntegerField(default=100)
    droplimit = models.SmallIntegerField(default=0)
    mindrop = models.SmallIntegerField(default=0)
    multiplier_min = models.SmallIntegerField(default=0)

    class Meta:
        db_table = 'eq_loottable_entries'
        unique_together = (('loottable', 'lootdrop'),)


def __str__(self):
    return self.name
