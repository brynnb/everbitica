# Generated by Django 3.2.25 on 2024-05-01 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('everbitica', '0007_races'),
    ]

    operations = [
        migrations.CreateModel(
            name='NpcTypes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('lastname', models.CharField(blank=True, max_length=32, null=True)),
                ('level', models.PositiveSmallIntegerField(default=0)),
                ('race', models.PositiveSmallIntegerField(default=0)),
                ('class_field', models.PositiveSmallIntegerField(db_column='class', default=0)),
                ('bodytype', models.IntegerField(default=1)),
                ('hp', models.IntegerField(default=0)),
                ('mana', models.IntegerField(default=0)),
                ('gender', models.PositiveSmallIntegerField(default=0)),
                ('texture', models.PositiveSmallIntegerField(default=0)),
                ('helmtexture', models.PositiveSmallIntegerField(default=0)),
                ('size', models.FloatField(default=0)),
                ('hp_regen_rate', models.PositiveIntegerField(default=0)),
                ('mana_regen_rate', models.PositiveIntegerField(default=0)),
                ('loottable_id', models.PositiveIntegerField(default=0)),
                ('merchant_id', models.PositiveIntegerField(default=0)),
                ('npc_spells_id', models.PositiveIntegerField(default=0)),
                ('npc_spells_effects_id', models.PositiveIntegerField(default=0)),
                ('npc_faction_id', models.IntegerField(default=0)),
                ('mindmg', models.PositiveIntegerField(default=0)),
                ('maxdmg', models.PositiveIntegerField(default=0)),
                ('attack_count', models.SmallIntegerField(default=-1)),
                ('special_abilities', models.TextField(blank=True, null=True)),
                ('aggroradius', models.PositiveIntegerField(default=0)),
                ('assistradius', models.PositiveIntegerField(default=0)),
                ('face', models.PositiveIntegerField(default=1)),
                ('luclin_hairstyle', models.PositiveIntegerField(default=1)),
                ('luclin_haircolor', models.PositiveIntegerField(default=1)),
                ('luclin_eyecolor', models.PositiveIntegerField(default=1)),
                ('luclin_eyecolor2', models.PositiveIntegerField(default=1)),
                ('luclin_beardcolor', models.PositiveIntegerField(default=1)),
                ('luclin_beard', models.PositiveIntegerField(default=0)),
                ('armortint_id', models.PositiveIntegerField(default=0)),
                ('armortint_red', models.PositiveSmallIntegerField(default=0)),
                ('armortint_green', models.PositiveSmallIntegerField(default=0)),
                ('armortint_blue', models.PositiveSmallIntegerField(default=0)),
                ('d_melee_texture1', models.IntegerField(default=0)),
                ('d_melee_texture2', models.IntegerField(default=0)),
                ('prim_melee_type', models.PositiveSmallIntegerField(default=28)),
                ('sec_melee_type', models.PositiveSmallIntegerField(default=28)),
                ('ranged_type', models.PositiveSmallIntegerField(default=7)),
                ('runspeed', models.FloatField(default=0)),
                ('MR', models.SmallIntegerField(default=0)),
                ('CR', models.SmallIntegerField(default=0)),
                ('DR', models.SmallIntegerField(default=0)),
                ('FR', models.SmallIntegerField(default=0)),
                ('PR', models.SmallIntegerField(default=0)),
                ('see_invis', models.SmallIntegerField(default=0)),
                ('see_invis_undead', models.SmallIntegerField(default=0)),
                ('qglobal', models.PositiveSmallIntegerField(default=0)),
                ('AC', models.SmallIntegerField(default=0)),
                ('npc_aggro', models.PositiveSmallIntegerField(default=0)),
                ('spawn_limit', models.PositiveSmallIntegerField(default=0)),
                ('attack_delay', models.PositiveSmallIntegerField(default=30)),
                ('STR', models.PositiveIntegerField(default=75)),
                ('STA', models.PositiveIntegerField(default=75)),
                ('DEX', models.PositiveIntegerField(default=75)),
                ('AGI', models.PositiveIntegerField(default=75)),
                ('_INT', models.PositiveIntegerField(db_column='INT', default=80)),
                ('WIS', models.PositiveIntegerField(default=75)),
                ('CHA', models.PositiveIntegerField(default=75)),
                ('see_sneak', models.PositiveSmallIntegerField(default=0)),
                ('see_improved_hide', models.PositiveSmallIntegerField(default=0)),
                ('ATK', models.PositiveIntegerField(default=0)),
                ('Accuracy', models.PositiveIntegerField(default=0)),
                ('slow_mitigation', models.SmallIntegerField(default=0)),
                ('maxlevel', models.PositiveSmallIntegerField(default=0)),
                ('scalerate', models.IntegerField(default=100)),
                ('private_corpse', models.PositiveSmallIntegerField(default=0)),
                ('unique_spawn_by_name', models.PositiveSmallIntegerField(default=0)),
                ('underwater', models.PositiveSmallIntegerField(default=0)),
                ('isquest', models.PositiveSmallIntegerField(default=0)),
                ('emoteid', models.PositiveIntegerField(default=0)),
                ('spellscale', models.FloatField(default=100)),
                ('healscale', models.FloatField(default=100)),
                ('raid_target', models.PositiveSmallIntegerField(default=0)),
                ('chesttexture', models.PositiveSmallIntegerField(default=0)),
                ('armtexture', models.PositiveSmallIntegerField(default=0)),
                ('bracertexture', models.PositiveSmallIntegerField(default=0)),
                ('handtexture', models.PositiveSmallIntegerField(default=0)),
                ('legtexture', models.PositiveSmallIntegerField(default=0)),
                ('feettexture', models.PositiveSmallIntegerField(default=0)),
                ('light', models.PositiveSmallIntegerField(default=0)),
                ('walkspeed', models.FloatField(default=0)),
                ('combat_hp_regen', models.IntegerField(default=0)),
                ('combat_mana_regen', models.IntegerField(default=0)),
                ('aggro_pc', models.PositiveSmallIntegerField(default=0)),
                ('ignore_distance', models.FloatField(default=600)),
                ('encounter', models.PositiveSmallIntegerField(default=0)),
                ('ignore_despawn', models.PositiveSmallIntegerField(default=0)),
                ('avoidance', models.SmallIntegerField(default=0)),
                ('exp_pct', models.PositiveSmallIntegerField(default=100)),
                ('greed', models.PositiveSmallIntegerField(default=0)),
                ('engage_notice', models.PositiveSmallIntegerField(default=0)),
                ('stuck_behavior', models.PositiveSmallIntegerField(default=0)),
                ('flymode', models.PositiveSmallIntegerField(default=-1)),
                ('skip_global_loot', models.PositiveSmallIntegerField(default=0)),
                ('rare_spawn', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'db_table': 'eq_npc_types',
            },
        ),
    ]
