import re

# List of tables you want to keep
tables_to_keep = ['books', 'char_create_combinations', 'char_create_point_allocations', 
                  'faction_list', 'Items', 'level_xp_mods', 'lootdrop', 'lootdrop_entries', 
                  'loottable', 'loottable_entries', 'npc_spells', 'npc_spells_effects', 
                  'npc_spells_effects_entries', 'npc_spells_entries', 'npc_types', 'races', 
                  'skill_caps', 'skill_difficulty', 'spawn2', 'spawnentry', 'spawngroup', 
                  'spells_en', 'spells_new', 'starting_items', 'start_zones', 
                  'tradeskill_recipe', 'tradeskill_recipe_entries', 'zone']

# Read the SQL file
with open('devassets/everquest_data.sql', 'r') as file:
    data = file.read()

# Split the data into separate tables
tables = re.split(r'CREATE TABLE', data)

# Filter out the tables you want to keep and rename them
filtered_tables = []
for table in tables:
    if any(name in table for name in tables_to_keep):
        for name in tables_to_keep:
            table = table.replace(name, 'eq_' + name)
        filtered_tables.append(table)

# Join the tables back into a single string
filtered_data = 'CREATE TABLE'.join(filtered_tables)

