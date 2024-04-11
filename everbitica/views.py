from django.shortcuts import render
from django.http import JsonResponse

from habitica import *
from .models import PlayerClass
import requests
import os
import habitica
import json
from habitica.common import HabiticaEndpointsProcessor
import time


def index(request):

    user_id = os.getenv("HABITICA_API_USER")
    api_key = os.getenv("HABITICA_API_KEY")

    habitica_client = habitica.Client(user_id, api_key)

    # load or fetch general game data
    saved_content = get_game_content()

    # there might be some overlap in this data, for example i think maybe chat data also comes with group data?
    quest_data = habitica_client.group.quest.get_info()
    group_data = habitica_client.group.get_info()
    chat_data = habitica_client.chat.get_all()
    user_data = habitica_client.user.get_user_info()

    habitica_client.chat.read_all()  # so it doesnt show as unread on direct habaitica site
    habitica_client.notification.read_all()

    total_items, total_boss_hp, current_target_name, target_percent_done = get_quest_progress(
        quest_data, saved_content
    )

    player_health_percent = user_data.data.stats.hp / user_data.data.stats.maxHealth
    player_mana_percent = user_data.data.stats.mp / user_data.data.stats.maxMP
    player_xp_percent = user_data.data.stats.exp / user_data.data.stats.toNextLevel
    player_xp_percent_subbar = (
        player_xp_percent % 0.2
    ) / 0.2  # how far into the current 1/5th segment the player is

    messages = format_messages(chat_data.data)

    # group_members = habitica_client.group.get_members()
    # print(group_members)

    return render(
        request,
        "index.html",
        {
            "user_data": user_data,
            "player_xp_percent": player_xp_percent,
            "player_health_percent": player_health_percent,
            "player_mana_percent": player_mana_percent,
            "messages": messages,
            "player_xp_percent_subbar": player_xp_percent_subbar,
            "current_target_name": current_target_name,
            "target_percent_done": target_percent_done,
        },
    )

# def get_group_members(group_data):
#     # get all group members and their class
#     group_members = {}
#     for member in group_data.data.members:
#         group_members[member.id] = member.profile.name

#     return group_members

def get_quest_progress(quest_data, saved_content):
    total_items = 0
    total_boss_hp = 0
    current_target_name = ""
    percent_done = 0
    current_quest_key = quest_data.data.quest.key
    if current_quest_key in saved_content.get("data", {}).get("quests", {}):
        current_quest_content = saved_content["data"]["quests"][current_quest_key]
        # determine if current_quest_content is a collect quest or boss
        if "collect" in current_quest_content:
            # loop through all child items of current_quest_content['collect']
            for key in current_quest_content["collect"]:
                # if the item is not found, set quest_key to the key of the first item not found
                total_items += current_quest_content["collect"][key]["count"]
        else:
            total_boss_hp = current_quest_content["boss"]["hp"]

    return total_items, total_boss_hp, current_target_name, percent_done


def format_messages(raw_messages):
    # create array of all messages along with the class (which indicates its color) it should be associated with
    messages = []

    for message in raw_messages:
        if hasattr(message, "info") and "type" in message.info:
            if message.info["type"] == "boss_damage":
                user_damage_messages = message.unformattedText.split(". ")

                messages.append(
                    {
                        "text": user_damage_messages[0] + ".",
                        "class": get_chat_class(message.info["type"]),
                    }
                )
                if len(user_damage_messages) > 1:
                    messages.append(
                        {
                            "text": user_damage_messages[1],
                            "class": "red-text",
                        }
                    )
            else:
                messages.append(
                    {
                        "text": message.unformattedText,
                        "class": get_chat_class(message.info["type"]),
                    }
                )

        elif hasattr(message, "userStyles"):
            messages.append(
                {
                    "text": message.user
                    + " tells the group, '"
                    + message.unformattedText
                    + "'",
                    "class": "teal-text",
                }
            )

        else:
            messages.append({"text": message.text, "class": get_chat_class("other")})

    # reverse order of messages
    return messages[::-1]


def get_chat_class(type):
    # map types to css classes for font colors
    chat_type_color_map = {
        "quest_start": "yellow-text",
        "boss_damage": "black-text",
        "boss_dont_attack": "black-text",
        "boss_rage": "red-text",
        "boss_defeated": "yellow-text",
        "user_found_items": "blue-text",
        "all_items_found": "yellow-text",
        "spell_cast_party": "blue-text",
        "spell_cast_user": "blue-text",
        "spell_cast_party_multi": "blue-text",
        "spell_cast_user_multi": "blue-text",
        "quest_cancel": "yellow-text",
        "quest_abort": "yellow-text",
        "tavern_quest_completed": "yellow-text",
        "tavern_boss_rage_tired": "red-text",
        "tavern_boss_rage": "red-text",
        "tavern_boss_desperation": "red-text",
        "claim_task": "yellow-text",
        "default": "black-text",
    }

    return chat_type_color_map.get(type, "black-text")


def get_game_content():
    # load all the of the "game content" like quests and item information
    try:
        with open("content.json", "r") as f:
            # throw exception if file is over a week old so it can be refreshed
            if os.path.getmtime("content.json") < time.time() - 604800:
                raise FileNotFoundError

            saved_content = json.load(f)
    except json.JSONDecodeError:  # fetch data if saved json doesn't exist
        not_auth_client = habitica.NotAuthClient()
        saved_content = not_auth_client.get_content()
        with open("content.json", "w") as f:
            json.dump(saved_content, f)

    return saved_content
