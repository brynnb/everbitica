from django.core.management.base import BaseCommand
from django.core.management import call_command
from everbitica.models import *
from django.db import connection
from django.core.management.base import CommandError
from dotenv import load_dotenv
import os


class Command(BaseCommand):
    help = "Runs all project setup tasks"

    def handle(self, *args, **options):
        load_dotenv()  # Load variables from .env file
        debug = os.getenv("DEBUG")

        # Don't allow outside dev env cus we're dropping tables which is potentianlly dangerous
        if not debug:
            raise CommandError(
                "This command cannot be run outside development environment."
            )

        # Drop all tables in database
        self.stdout.write(self.style.SUCCESS("Dropping all tables in database..."))
        with connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")  # Disable foreign key checks
            cursor.execute("SHOW TABLES")  # Get a list of all table names
            tables = cursor.fetchall()
            for table in tables:
                cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")  # Drop each table
            cursor.execute(
                "SET FOREIGN_KEY_CHECKS = 1;"
            )  # Re-enable foreign key checks

        # Import EverQuest data
        self.stdout.write(self.style.SUCCESS("Importing EverQuest data..."))
        call_command("seed_eq_data_tables")

        # Make migrations
        self.stdout.write(self.style.SUCCESS("Creating migrations..."))
        call_command("makemigrations")

        # Migrate
        self.stdout.write(self.style.SUCCESS("Migrating..."))
        call_command("migrate")

        # Seed additional EQ data
        self.stdout.write(self.style.SUCCESS("Seeding additional EQ data..."))
        call_command("seed_additional_eq_data")

        self.stdout.write(self.style.SUCCESS("Successfully ran project setup tasks!"))
