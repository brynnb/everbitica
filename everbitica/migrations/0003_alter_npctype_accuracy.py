# Generated by Django 3.2.25 on 2024-05-08 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('everbitica', '0002_alter_npctype_atk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='npctype',
            name='Accuracy',
            field=models.BigIntegerField(default=0),
        ),
    ]