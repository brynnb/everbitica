from enum import Enum

# auth fields
USER_ID = "user_id"
TOKEN = "token"
USER_NAME = "user_name"

# invitation types

PARTIES = "parties"
PARTY = "party"
GUILDS = "guilds"
TAVERN = "tavern"


class TaskType(str, Enum):
    HABIT = "habit"
    DAILY = "daily"
    TODO = "todo"
    REWARD = "reward"
    COMPLETED = "completedTodo"


class AttributeType(str, Enum):
    STR = "str"
    INT = "int"
    PER = "per"
    CON = "con"


class PriorityType(float, Enum):
    EASY = "0.1"
    MEDIUM = "1"
    HARD = "1.5"
    LEGENDARY = "2"


class FrequencyType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class GroupType(str, Enum):
    GUILD = "guild"
    PARTY = "party"


class DirectionType(str, Enum):
    UP = "up"
    DOWN = "down"


class Privacy(str, Enum):
    PRIVATE = "private"
    PUBLIC = "public"


class NotificationType(str, Enum):
    CARD_RECEIVED = "CARD_RECEIVED"
    CRON = "CRON"
    DROP_CAP_REACHED = "DROP_CAP_REACHED"
    FIRST_DROPS = "FIRST_DROPS"
    GIFT_ONE_GET_ONE = "GIFT_ONE_GET_ONE"
    GROUP_INVITE_ACCEPTED = "GROUP_INVITE_ACCEPTED"
    GROUP_TASK_APPROVAL = "GROUP_TASK_APPROVAL"
    GROUP_TASK_APPROVED = "GROUP_TASK_APPROVED"
    GROUP_TASK_ASSIGNED = "GROUP_TASK_ASSIGNED"
    GROUP_TASK_CLAIMED = "GROUP_TASK_CLAIMED"
    GROUP_TASK_NEEDS_WORK = "GROUP_TASK_NEEDS_WORK"
    GUILD_PROMPT = "GUILD_PROMPT"
    LOGIN_INCENTIVE = "LOGIN_INCENTIVE"
    NEW_CHAT_MESSAGE = "NEW_CHAT_MESSAGE"
    NEW_CONTRIBUTOR_LEVEL = "NEW_CONTRIBUTOR_LEVEL"
    NEW_INBOX_MESSAGE = "NEW_INBOX_MESSAGE"
    NEW_MYSTERY_ITEMS = "NEW_MYSTERY_ITEMS"
    NEW_STUFF = "NEW_STUFF"
    ONBOARDING_COMPLETE = "ONBOARDING_COMPLETE"
    REBIRTH_ENABLED = "REBIRTH_ENABLED"
    SCORED_TASK = "SCORED_TASK"
    UNALLOCATED_STATS_POINTS = "UNALLOCATED_STATS_POINTS"
    WON_CHALLENGE = "WON_CHALLENGE"
    # achievement notifications
    ACHIEVEMENT = "ACHIEVEMENT"
    CHALLENGE_JOINED_ACHIEVEMENT = "CHALLENGE_JOINED_ACHIEVEMENT"
    GUILD_JOINED_ACHIEVEMENT = "GUILD_JOINED_ACHIEVEMENT"
    ACHIEVEMENT_PARTY_ON = "ACHIEVEMENT_PARTY_ON"
    ACHIEVEMENT_PARTY_UP = "ACHIEVEMENT_PARTY_UP"
    INVITED_FRIEND_ACHIEVEMENT = "INVITED_FRIEND_ACHIEVEMENT"
    REBIRTH_ACHIEVEMENT = "REBIRTH_ACHIEVEMENT"
    STREAK_ACHIEVEMENT = "STREAK_ACHIEVEMENT"
    ULTIMATE_GEAR_ACHIEVEMENT = "ULTIMATE_GEAR_ACHIEVEMENT"
    ACHIEVEMENT_STABLE = "ACHIEVEMENT_STABLE"
    ACHIEVEMENT_QUESTS = "ACHIEVEMENT_QUESTS"
    ACHIEVEMENT_ANIMAL_SET = "ACHIEVEMENT_ANIMAL_SET"
    ACHIEVEMENT_PET_COLOR = "ACHIEVEMENT_PET_COLOR"
    ACHIEVEMENT_MOUNT_COLOR = "ACHIEVEMENT_MOUNT_COLOR"


# leave group settings
class KeepType(Enum):
    REMOVE_ALL = "remove-all"
    KEEP_ALL = "keep-all"


class KeepChallengesType(Enum):
    REMAIN_IN_CHALLENGES = "remain-in-challenges"
    LEAVE_CHALLENGES = "leave-challenges"


class SpellType(str, Enum):
    FIREBALL = "fireball"
    MP_HEAL = "mpheal"
    EARTH = "earth"
    FROST = "frost"
    SMASH = "smash"
    DEFENSIVE_STANCE = "defensiveStance"
    VALOROUS_PRESENCE = "valorousPresence"
    INTIMIDATE = "intimidate"
    PICK_POCKET = "pickPocket"
    BACK_STAB = "backStab"
    TOOLS_OF_TRADE = "toolsOfTrade"
    STEALTH = "stealth"
    HEAL = "heal"
    PROTECT_AURA = "protectAura"
    BRIGHTNESS = "brightness"
    HEAL_ALL = "healAll"
    SNOWBALL = "snowball"
    SPOOKY_SPARKLES = "spookySparkles"
    SEAFOAM = "seafoam"
    SHINY_SEED = "shinySeed"


class ClassType(str, Enum):
    WARRIOR = "warrior"
    ROUGE = "rogue"
    WIZARD = "wizard"
    HEALER = "healer"


class EquipType(str, Enum):
    MOUNT = "mount"
    PET = "pet"
    COSTUME = "costume"
    EQUIPPED = "equipped"
