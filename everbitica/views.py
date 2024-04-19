import random
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
    """Main view for the app. This view will fetch all data needed for the UI, including player stats, chat messages, and quest progress. It will then render the index.html template with this data. If the app is in offline mode, it will attempt to load the view data from a json file. If the file does not exist, it will return an error message."""

    offline_mode = os.getenv("OFFLINE_MODE")
    # offline_mode = False
    offline_mode = True

    if not offline_mode:
        view_data = get_all_ui_data()

    else:
        # attempt to load view_data from json file
        try:
            with open("view_data.json", "r") as f:
                view_data = json.load(f)
        except FileNotFoundError:
            return JsonResponse({"error": "No offline data available."})

    # group_members = habitica_client.group.get_members()
    # print(group_members)

    return render(request, "index.html", view_data)


def get_party_members():
    habitica_client = get_habitica_client()
    party_members = habitica_client.group.get_members().data

    party_members = sorted(
        party_members, key=lambda x: x["auth"]["timestamps"]["updated"], reverse=True
    )

    simplified_members = []
    for member in party_members:
        simplified_members.append(
            {
                "hp": member["stats"]["hp"],
                "mp": member["stats"]["mp"],
                "maxMP": member["stats"]["maxMP"],
                "maxHealth": member["stats"]["maxHealth"],
                "username": member["auth"]["local"]["username"],
                "healthPercent": member["stats"]["hp"] / member["stats"]["maxHealth"],
            }
        )

    return simplified_members


def get_habitica_client():
    user_id = os.getenv("HABITICA_API_USER")
    api_key = os.getenv("HABITICA_API_KEY")

    return habitica.Client(user_id, api_key)


def get_all_ui_data():
    """Get all data needed for the UI, including player stats, chat messages, and quest progress."""
    habitica_client = get_habitica_client()

    # load or fetch general game data
    saved_content = get_game_content()

    # there might be some overlap in this data, for example i think maybe chat data also comes with group data?
    quest_data = habitica_client.group.quest.get_info()
    group_data = habitica_client.group.get_info()
    chat_data = habitica_client.chat.get_all()
    user_data = habitica_client.user.get_user_info()

    habitica_client.chat.read_all()  # so it doesnt show as unread on direct habaitica site
    habitica_client.notification.read_all()

    total_items, total_boss_hp, current_target_name, target_percent_done = (
        get_quest_progress(quest_data, saved_content)
    )

    messages = format_messages(chat_data.data)
    player_data = get_player_stats(user_data)

    view_data = {
        "player_data": player_data,
        "messages": messages,
        "current_target_name": current_target_name,
        "target_percent_done": target_percent_done,
        "spell_gems": get_spell_gems(),
        "video_embed_url": get_video_embed_option(),
        "party_members": get_party_members()
    }

    # save all view data to json to retrieve later in offline mode
    with open("view_data.json", "w") as f:
        json.dump(view_data, f)

    return view_data


def get_video_embed_option():
    """Return a random youtube video URL with specific parameters to autoplay, loop, and start at a random time."""

    base_str = "https://www.youtube.com/embed/?autoplay=1&mute=1&loop=1&playlist="
    end_str = "&start="

    # list of youtube video URLS and start and end of acceptable "start" times to randomly choose between
    video_options = [
        {"video_code": "awN7hdTfivE", "start": 0, "end": 21291},
        {"video_code": "egErjaxXK-c", "start": 0, "end": 1587},
        {"video_code": "eudivHLEg-4", "start": 0, "end": 600},
        {"video_code": "1dZ9XQTwmXA", "start": 0, "end": 600},
        {"video_code": "lfQpJRqNEho", "start": 0, "end": 500},
        {"video_code": "ImdkeY1pz_k", "start": 0, "end": 500},
        {"video_code": "ac68dDjQZGc", "start": 0, "end": 500},
        {"video_code": "2__FZLzOLpw", "start": 0, "end": 500},
        {"video_code": "Gap_QOG5MLI", "start": 0, "end": 500},
        {"video_code": "Gw2N-pUlvv8", "start": 0, "end": 500},
        {"video_code": "NzAUeS24Kwc", "start": 0, "end": 500},
        {"video_code": "NZ4c6jO0qNs", "start": 0, "end": 500},
        {"video_code": "ekLYIiWiWDc", "start": 0, "end": 500},
        {"video_code": "L3FYvLQL_zM", "start": 0, "end": 500},
        {"video_code": "GvIfsfZfstk", "start": 0, "end": 500},
        {"video_code": "sWPAYwQltJk", "start": 0, "end": 500},
        {
            "video_code": "5rwybDHusTg",
            "start": 0,
            "end": 500,
        },  # East Freeport Camp - EQ Music & Ambiance
        {
            "video_code": "zjt1Oo7oZts",
            "start": 0,
            "end": 500,
        },  # Toxxulia Forest - EQ Music & Ambiance
        {
            "video_code": "_x-B1hHtqeE",
            "start": 0,
            "end": 500,
        },  # Freeport Docks - EQ Music & Ambiance
        {
            "video_code": "KL_bAUH2-b4",
            "start": 0,
            "end": 500,
        },  # Oasis of Marr - EQ Music & Ambiance
        {
            "video_code": "mzysKHdgrI4",
            "start": 0,
            "end": 500,
        },  # High Keep - EQ Music & Ambiance
        {
            "video_code": "ZPikCYEKFSM",
            "start": 0,
            "end": 500,
        },  # Kerra Isle - EQ Music & Ambiance
        {
            "video_code": "4qSq49a38wE",
            "start": 0,
            "end": 500,
        },  #  Qeynos Hills Hut - EQ Music & Ambiance
        {"video_code": "5Fw7FKvU4L0", "start": 0, "end": 500},  # Surefall Glade
        {
            "video_code": "wghCyEQQlLo",
            "start": 0,
            "end": 500,
        },  #  Surefall Glade Druids - EQ Music & Ambiance
        {
            "video_code": "Sh20g9lxXKg",
            "start": 0,
            "end": 500,
        },  #  Thurgadin - EQ Music & Ambiance
        {
            "video_code": "lQyn9moWEFM",
            "start": 0,
            "end": 500,
        },  #  Qeynos Hills - EQ Music & Ambiance
        {
            "video_code": "wioYS1RvvbU",
            "start": 0,
            "end": 500,
        },  #  Blackburrow - EQ Music & Ambiance
        {
            "video_code": "mu4f6dxsGSw",
            "start": 0,
            "end": 500,
        },  #  Freeport Bank - EQ Music & Ambiance
        {
            "video_code": "GIvnzQxO9MY",
            "start": 0,
            "end": 500,
        },  #  Halas - EQ Music & Ambiance
        {
            "video_code": "KHXgjHtG0aE",
            "start": 0,
            "end": 500,
        },  #  Northern Desert of Ro - EQ Music & Ambiance
        {
            "video_code": "2uA3aXQbLuE",
            "start": 0,
            "end": 500,
        },  #  Ak'Anon - EQ Music & Ambiance
        {
            "video_code": "_Vo90Ld9BVQ",
            "start": 0,
            "end": 500,
        },  #  Freeport Academy - EQ Music & Ambiance
        {
            "video_code": "5S4joYtfzGQ",
            "start": 0,
            "end": 500,
        },  #  West Karanas - EQ Music & Ambiance
        {
            "video_code": "5ONH2utKeFg",
            "start": 0,
            "end": 500,
        },  #  Felwithe - EQ Music & Ambiance
        {
            "video_code": "OLdxeNm9umQ",
            "start": 0,
            "end": 500,
        },  #  Rivervale - EQ Music & Ambiance
        {
            "video_code": "qK9ie3pjp6w",
            "start": 0,
            "end": 500,
        },  #  West Freeport - EQ Music & Ambiance
    ]
    # randomly choose a video to embed
    video_choice = random.choice(video_options)
    # choose random start time between start and end
    start_time = random.randint(video_choice["start"], video_choice["end"])

    # combine base, video code, end, and start time to return the full URL
    video_url = base_str + video_choice["video_code"] + end_str + str(start_time)

    return video_url


def get_player_stats(user_data):
    """Get player stats and return them as a dictionary."""
    health_percent = user_data.data.stats.hp / user_data.data.stats.maxHealth
    mana_percent = user_data.data.stats.mp / user_data.data.stats.maxMP
    xp_percent = user_data.data.stats.exp / user_data.data.stats.toNextLevel
    xp_percent_subbar = (
        xp_percent % 0.2
    ) / 0.2  # how far into the current 1/5th segment the player is

    # combine all into a single dictionary to return
    player_data = {
        "health_percent": health_percent,
        "mana_percent": mana_percent,
        "xp_percent": xp_percent,
        "xp_percent_subbar": xp_percent_subbar,
        "name": user_data.data.profile.name,
    }

    return player_data


# def get_group_members(group_data):
#     # get all group members and their class
#     group_members = {}
#     for member in group_data.data.members:
#         group_members[member.id] = member.profile.name

#     return group_members


def get_spell_gems():
    """Return a dictionary of all spell gems and their spritesheet coordinates."""
    spell_gems = {
        "1": {"spritesheet": "gemicons01.png", "x": 1, "y": 0},
        "2": {"spritesheet": "gemicons01.png", "x": -37, "y": 0},
        "3": {"spritesheet": "gemicons01.png", "x": -74, "y": 0},
        "4": {"spritesheet": "gemicons01.png", "x": -111, "y": 0},
        "5": {"spritesheet": "gemicons01.png", "x": -148, "y": 0},
        "6": {"spritesheet": "gemicons01.png", "x": -185, "y": 0},
        "7": {"spritesheet": "gemicons01.png", "x": -222, "y": 0},
        "8": {"spritesheet": "gemicons01.png", "x": -222, "y": -28},
    }

    return spell_gems


def get_quest_progress(quest_data, saved_content):
    """Get the current quest progress and return the total items needed, total boss hp, current boss name, and percent done."""
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
            current_boss_hp = quest_data.data.quest.progress.hp

            if (
                current_boss_hp is not None
                and total_boss_hp is not None
                and total_boss_hp > 0
            ):
                percent_done = current_boss_hp / total_boss_hp

            current_target_name = current_quest_content["boss"]["name"]

    return total_items, total_boss_hp, current_target_name, percent_done


def format_messages(raw_messages):
    """create array of all messages along with the class (which indicates its color) it should be associated with"""
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
    """load all the of the static game content like quests and item information"""
    try:
        with open("content.json", "r") as f:
            # throw exception if file is over a week old so it can be refreshed
            if os.path.getmtime("content.json") < time.time() - 604800:
                raise FileNotFoundError

            saved_content = json.load(f)
    except FileNotFoundError:
        saved_content = fetch_and_save_content()
    except (
        json.JSONDecodeError
    ):  # fetch data if saved json doesn't exist or is not valid
        saved_content = fetch_and_save_content()

    return saved_content


def fetch_and_save_content():
    not_auth_client = habitica.NotAuthClient()
    content = not_auth_client.get_content()
    with open("content.json", "w") as f:
        json.dump(content, f)
    return content
