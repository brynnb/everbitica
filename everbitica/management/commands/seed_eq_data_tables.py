from django.core.management.base import BaseCommand, CommandError
from django.db import connection
import re
import os
from dotenv import load_dotenv


""" 
As a backup if this doesn't work or becomes buggy:

Copy and paste the devassets/everquest_data.sql to your docker container, somewhere like "/tmp", then:

docker exec -it 1d0 /bin/bash -c "mysql -u user_name -puser_password database_name < /tmp/everquest_data.sql" 

everquest_data.sql was downloaded from the TAKP project here: https://github.com/EQMacEmu/Server/tree/main/utils/sql/database_full/

It was then modified to remove comments since they were throwing errors when trying to import the data, but it's unclear if that would be needed with the import command in its current form

"""


class Command(BaseCommand):
    help = "Import EverQuest data"

    def handle(self, *args, **options):
        load_dotenv()  # Load variables from .env file
        debug = os.getenv("DEBUG")

        # Don't allow outside dev env cus we're dropping tables which is potentianlly dangerous
        if not debug:
            raise CommandError(
                "This command cannot be run outside development environment."
            )

        # drop all existing eq_ prefix tables
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES LIKE 'eq_%'")
            tables = cursor.fetchall()
            for table in tables:
                cursor.execute(f"DROP TABLE {table[0]}")

        # List of tables to keep
        tables_to_keep = [
            "books",
            "char_create_combinations",
            "char_create_point_allocations",
            "faction_list",
            "Items",
            "level_xp_mods",
            "lootdrop",
            "lootdrop_entries",
            "loottable",
            "loottable_entries",
            "npc_spells",
            "npc_spells_effects",
            "npc_spells_effects_entries",
            "npc_spells_entries",
            "npc_types",
            "races",
            "skill_caps",
            "skill_difficulty",
            "spawn2",
            "spawnentry",
            "spawngroup",
            "spells_en",
            "spells_new",
            "starting_items",
            "start_zones",
            "tradeskill_recipe",
            "tradeskill_recipe_entries",
            "zone",
        ]

        # Read the SQL file
        with open("devassets/everquest_data.sql", "r") as file:
            data = file.read()

        # Split the data into separate tables
        tables = re.split(r"CREATE TABLE", data)

        # Filter out the tables to keep and rename them
        filtered_tables = []
        for table in tables:
            # Get the table name from the start of the table string
            table_name = table.split()

            if table_name:
                table_name = table_name[0]
                # remove backticks from table_name
                table_name = table_name.replace("`", "")

            else:
                continue

            if table_name in tables_to_keep:

                # rename table and use replace function but only if it also includes the "`" characters
                table = table.replace("`" + table_name + "`", "`eq_" + table_name + "`")
                filtered_tables.append("CREATE TABLE " + table)

        # Join the tables back into a single string
        filtered_data = "\n".join(filtered_tables)

        # Split the filtered_data into separate commands
        commands = filtered_data.split(";\n")

        # Execute each command individually
        with connection.cursor() as cursor:
            for command in commands:
                if command.strip():  # Make sure the command is not empty
                    cursor.execute(command)

        self.stdout.write(self.style.SUCCESS("Successfully imported EverQuest data"))
