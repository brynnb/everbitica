# Generated by Django 3.2.25 on 2024-05-01 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('everbitica', '0009_alter_npctypes_flymode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Spawn',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('spawngroupID', models.IntegerField(default=0)),
                ('zone', models.CharField(blank=True, max_length=32, null=True)),
                ('x', models.FloatField(default=0.0)),
                ('y', models.FloatField(default=0.0)),
                ('z', models.FloatField(default=0.0)),
                ('heading', models.FloatField(default=0.0)),
                ('respawntime', models.IntegerField(default=0)),
                ('variance', models.IntegerField(default=0)),
                ('pathgrid', models.IntegerField(default=0)),
                ('_condition', models.PositiveIntegerField(default=0)),
                ('cond_value', models.IntegerField(default=1)),
                ('enabled', models.PositiveSmallIntegerField(default=1)),
                ('animation', models.PositiveSmallIntegerField(default=0)),
                ('boot_respawntime', models.IntegerField(default=0)),
                ('clear_timer_onboot', models.PositiveSmallIntegerField(default=0)),
                ('boot_variance', models.IntegerField(default=0)),
                ('force_z', models.PositiveSmallIntegerField(default=0)),
                ('min_expansion', models.SmallIntegerField(default=-1)),
                ('max_expansion', models.SmallIntegerField(default=-1)),
                ('content_flags', models.CharField(blank=True, max_length=100, null=True)),
                ('content_flags_disabled', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'eq_spawn2',
            },
        ),
        migrations.CreateModel(
            name='Spawnentry',
            fields=[
                ('spawngroupID', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('npcID', models.IntegerField(default=0)),
                ('chance', models.SmallIntegerField(default=0)),
                ('mintime', models.SmallIntegerField(default=0)),
                ('maxtime', models.SmallIntegerField(default=0)),
                ('min_expansion', models.SmallIntegerField(default=-1)),
                ('max_expansion', models.SmallIntegerField(default=-1)),
                ('content_flags', models.CharField(blank=True, max_length=100, null=True)),
                ('content_flags_disabled', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'eq_spawnentry',
            },
        ),
        migrations.CreateModel(
            name='Spawngroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=50, unique=True)),
                ('spawn_limit', models.SmallIntegerField(default=0)),
                ('max_x', models.FloatField(default=0.0)),
                ('min_x', models.FloatField(default=0.0)),
                ('max_y', models.FloatField(default=0.0)),
                ('min_y', models.FloatField(default=0.0)),
                ('delay', models.IntegerField(default=45000)),
                ('mindelay', models.IntegerField(default=15000)),
                ('despawn', models.PositiveSmallIntegerField(default=0)),
                ('despawn_timer', models.IntegerField(default=100)),
                ('rand_spawns', models.IntegerField(default=0)),
                ('rand_respawntime', models.IntegerField(default=1200)),
                ('rand_variance', models.IntegerField(default=0)),
                ('rand_condition', models.IntegerField(default=0)),
                ('wp_spawns', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'db_table': 'eq_spawngroup',
            },
        ),
        migrations.RenameModel(
            old_name='Books',
            new_name='Book',
        ),
        migrations.RenameModel(
            old_name='NpcTypes',
            new_name='NpcType',
        ),
        migrations.RenameModel(
            old_name='Races',
            new_name='Race',
        ),
    ]