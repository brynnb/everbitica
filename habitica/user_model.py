from typing import Any, Dict, List, Optional

from pydantic import Field
from pydantic.datetime_parse import datetime
from pydantic.types import UUID4

from habitica.consts import ClassType
from habitica.common_model import HabiticaBaseModel, Response
from habitica.notification_model import Notification
from habitica.tag_model import Tag


class Local(HabiticaBaseModel):
    username: str
    lower_case_username: Optional[str]
    email: Optional[str]
    has_password: Optional[bool]


class Timestamps(HabiticaBaseModel):
    created: str
    logged_in: Optional[str]
    updated: str


class Auth(HabiticaBaseModel):
    local: Local
    timestamps: Timestamps
    facebook: Optional[Dict[str, Any]]
    google: Optional[Dict[str, Any]]
    apple: Optional[Dict[str, Any]]


class UltimateGearSets(HabiticaBaseModel):
    healer: bool
    wizard: bool
    rogue: bool
    warrior: bool


class Achievements(HabiticaBaseModel):
    ultimate_gear_sets: UltimateGearSets
    streak: int
    challenges: List
    perfect: int
    quests: Optional[Dict[str, Any]]
    party_up: bool
    created_task: Optional[bool]
    completed_task: Optional[bool]
    purchased_equipment: Optional[bool]


class Consecutive(HabiticaBaseModel):
    count: int
    offset: int
    gem_cap_extra: int
    trinkets: int


class Plan(HabiticaBaseModel):
    consecutive: Consecutive
    quantity: int
    extra_months: int
    gems_bought: int
    mystery_items: List
    date_updated: str


class Purchased(HabiticaBaseModel):
    ads: bool
    txn_count: int = Field(..., alias="txnCount")
    skin: Dict[str, Any]
    hair: Dict[str, Any]
    shirt: Dict[str, Any]
    background: Dict[str, Any]
    plan: Plan


class Flags(HabiticaBaseModel):
    tour: Optional[Dict]
    tutorial: Optional[Dict]
    customizations_notification: Optional[bool]
    show_tour: Optional[bool]
    drops_enabled: Optional[bool]
    items_enabled: Optional[bool]
    rewrite: Optional[bool]
    class_selected: Optional[bool]
    rebirth_enabled: Optional[bool]
    welcomed: Optional[bool]
    armoire_enabled: Optional[bool]
    armoire_opened: Optional[bool]
    armoire_empty: Optional[bool]
    card_received: Optional[bool]
    warned_low_health: Optional[bool]
    verified_username: Optional[bool]
    new_stuff: Optional[bool]
    community_guidelines_accepted: Optional[bool]
    recapture_emails_phase: Optional[int]
    weekly_recap_emails_phase: Optional[int]
    cron_count: Optional[int]
    level_drops: Optional[Dict]
    last_weekly_recap: Optional[datetime]


class History(HabiticaBaseModel):
    exp: List  # Todo: List of events?
    todos: List


class Equipped(HabiticaBaseModel):
    armor: str = Field(default=None)
    head: str = Field(default=None)
    shield: str = Field(default=None)
    weapon: str = Field(default=None)


class Costume(HabiticaBaseModel):
    armor: str
    head: str
    shield: str


class Gear(HabiticaBaseModel):
    equipped: Equipped = Field(default=None)
    costume: Costume = Field(default=None)
    owned: Dict[str, Any] = Field(default=None)


class Special(HabiticaBaseModel):
    snowball: int
    spooky_sparkles: int
    shiny_seed: int
    seafoam: int
    valentine: int
    valentine_received: List
    nye: int
    nye_received: List
    greeting: int
    greeting_received: List
    thankyou: int
    thankyou_received: List
    birthday: int
    birthday_received: List
    congrats: int
    congrats_received: List
    get_well: int
    get_well_received: List
    good_luck: int
    good_luck_received: List


class LastDrop(HabiticaBaseModel):
    count: int
    date: str


class Eggs(HabiticaBaseModel):
    # TODO What to do with new eggs
    fox: int


class HatchingPotions(HabiticaBaseModel):
    # TODO What to do with new potions
    royal_purple: int
    white: int
    zombie: int


class Food(HabiticaBaseModel):
    chocolate: int
    meat: int
    cotton_candy_pink: int
    cotton_candy_blue: int
    rotten_meat: int


class Items(HabiticaBaseModel):
    gear: Gear = Field(default=None)
    # special: Special
    special: Dict[str, Any] = Field(default=None)
    last_drop: LastDrop = Field(default=None)
    pets: Dict[str, Any] = Field(default=None)
    # eggs: Eggs
    eggs: Dict[str, Any] = Field(default=None)
    # hatching_potions: HatchingPotions
    hatching_potions: Dict[str, Any] = Field(default=None)
    # food: Food
    food: Dict[str, Any] = Field(default=None)
    mounts: Dict[str, Any] = Field(default=None)
    quests: Dict[str, Any] = Field(default=None)


class Invitations(HabiticaBaseModel):
    guilds: List
    party: Dict[str, Any]
    parties: List


class Progress(HabiticaBaseModel):
    up: int
    down: int
    collected_items: int
    collect: Optional[Dict[str, Any]]


class Quest(HabiticaBaseModel):
    progress: Optional[Progress]
    rsvp_needed: Optional[bool]


class Party(HabiticaBaseModel):
    id: UUID4 = Field(alias="_id", default=None)
    quest: Quest
    order: str
    order_ascending: str


class Hair(HabiticaBaseModel):
    color: str
    base: int
    bangs: int
    beard: int
    mustache: int
    flower: int


class EmailNotificationsPreferences(HabiticaBaseModel):
    unsubscribe_from_all: bool
    new_pm: Optional[bool] = None
    kicked_group: bool
    won_challenge: bool
    gifted_gems: bool
    gifted_subscription: bool
    invited_party: bool
    invited_guild: bool
    quest_started: bool
    invited_quest: bool
    important_announcements: bool
    weekly_recaps: bool
    onboarding: bool
    major_updates: bool
    subscription_reminders: bool


class PushNotificationsPreferences(HabiticaBaseModel):
    unsubscribe_from_all: bool
    new_pm: Optional[bool] = None
    won_challenge: bool
    gifted_gems: bool
    gifted_subscription: bool
    invited_party: bool
    invited_guild: bool
    quest_started: bool
    invited_quest: bool
    major_updates: bool
    mention_party: bool
    mention_joined_guild: bool
    mention_unjoined_guild: bool
    party_activity: bool


class SuppressModalsPreferences(HabiticaBaseModel):
    level_up: bool
    hatch_pet: bool
    raise_pet: bool
    streak: bool


class TaskPreferences(HabiticaBaseModel):
    group_by_challenge: bool
    confirm_score_notes: bool


class Preferences(HabiticaBaseModel):
    hair: Hair = Field(default=None)
    email_notifications: Optional[EmailNotificationsPreferences] = Field(default=None)
    push_notifications: Optional[PushNotificationsPreferences] = Field(default=None)
    suppress_modals: SuppressModalsPreferences = Field(default=None)
    tasks: TaskPreferences = Field(default=None)
    day_start: int = Field(default=None)
    size: str = Field(default=None)
    hide_header: bool = Field(default=None)
    skin: str = Field(default=None)
    shirt: str = Field(default=None)
    timezone_offset: int = Field(default=None)
    sound: str = Field(default=None)
    sound: str = Field(default=None)
    chair: str = Field(default=None)
    allocation_mode: str = Field(default=None)
    auto_equip: bool = Field(default=None)
    date_format: str = Field(default=None)
    sleep: bool = Field(default=None)
    sticky_header: bool = Field(default=None)
    disable_classes: bool = Field(default=None)
    new_task_edit: bool = Field(default=None)
    daily_due_default_view: bool = Field(default=None)
    advanced_collapsed: bool = Field(default=None)
    toolbar_collapsed: bool = Field(default=None)
    reverse_chat_order: bool = Field(default=None)
    display_invite_to_party_when_party_is1: bool = Field(default=None)
    improvement_categories: List = Field(default=None)
    language: str = Field(default=None)
    webhooks: Dict[str, Any] = Field(default=None)
    background: str = Field(default=None)
    timezone_offset_at_last_cron: int = Field(default=None)


class Profile(HabiticaBaseModel):
    name: str


class Buffs(HabiticaBaseModel):
    strength: float = Field(default=None, alias="str")
    constitution: float = Field(default=None, alias="con")
    intelligence: float = Field(default=None, alias="int")
    perception: float = Field(default=None, alias="per")
    stealth: int = Field(default=None)
    streaks: bool = Field(default=None)
    snowball: bool = Field(default=None)
    spooky_sparkles: bool = Field(default=None)
    shiny_seed: bool = Field(default=None)
    seafoam: bool = Field(default=None)


class Training(HabiticaBaseModel):
    strength: float = Field(alias="str")
    constitution: float = Field(alias="con")
    intelligence: float = Field(alias="int")
    perception: float = Field(alias="per")


class Stats(HabiticaBaseModel):
    buffs: Buffs = Field(default=None)
    training: Training = Field(default=None)
    hp: float = Field(default=None)
    mp: float = Field(default=None)
    exp: float = Field(default=None)
    gp: float = Field(default=None)
    lvl: float = Field(default=None)
    toNextLevel: float = Field(default=None)
    points: float = Field(default=None)
    strength: float = Field(default=None, alias="str")
    constitution: float = Field(default=None, alias="con")
    intelligence: float = Field(default=None, alias="int")
    perception: float = Field(default=None, alias="per")
    maxHealth: float = Field(default=None)
    maxMP: Optional[float] = Field(default=None)
    user_class: ClassType = Field(default=None, alias="user_class")

class Inbox(HabiticaBaseModel):
    newMessages: Optional[int]
    optOut: Optional[bool]
    blocks: Optional[List]
    messages: Optional[Dict]


class TasksOrder(HabiticaBaseModel):
    habits: List
    dailys: List
    todos: List
    rewards: List


class Item(HabiticaBaseModel):
    type: str = Field(default=None)  # TODO maybe enum
    path: str = Field(default=None)


class SleepWakeUpResponse(Response):
    data: bool


class UserInfo(HabiticaBaseModel):
    auth: Auth
    achievements: Achievements = Field(default=None)
    backer: Optional[Dict[str, Any]]
    contributor: Optional[Dict[str, Any]]
    permissions: Optional[Dict[str, Any]]
    purchased: Optional[Purchased]
    flags: Optional[Flags]
    history: Optional[History]
    items: Items
    invitations: Optional[Invitations]
    party: Party
    preferences: Preferences
    profile: Profile
    stats: Stats
    inbox: Inbox
    tasks_order: Optional[TasksOrder]
    # _v: int
    balance: Optional[int]
    challenges: Optional[List]
    guilds: Optional[List]
    login_incentives: int
    invites_sent: Optional[int]
    pinned_items_order: Optional[List]
    secret_id: UUID4 = Field(alias="_id")
    last_cron: Optional[str]
    new_messages: Optional[Dict[str, Any]]
    notifications: Optional[List[Notification]]
    tags: Optional[List[Tag]]
    extra: Optional[Dict[str, Any]]
    push_devices: Optional[List]
    webhooks: Optional[List]
    pinned_items: Optional[List[Item]]
    unpinned_items: Optional[List]
    migration: Optional[str]
    id: UUID4
    needs_cron: Optional[bool]


class GetUserInfoResponse(Response):
    data: UserInfo


class HatchPetResponse(Response):
    data: Items


class AchievementEvent(HabiticaBaseModel):
    title: str
    text: str
    icon: str
    earned: bool
    value: Optional[int]
    index: int
    optional_count: Optional[int]


class SpecialAchievements(HabiticaBaseModel):
    habit_surveys: AchievementEvent
    contributor: AchievementEvent


class SpecialAchievement(HabiticaBaseModel):
    label: str
    achievements: SpecialAchievements


class SeasonalAchievements(HabiticaBaseModel):
    habitica_days: AchievementEvent
    habit_birthdays: AchievementEvent
    snowball: AchievementEvent
    spooky_sparkles: AchievementEvent
    shiny_seed: AchievementEvent
    seafoam: AchievementEvent
    costume_contests: AchievementEvent
    nye_cards: AchievementEvent
    valentine_cards: AchievementEvent


class Seasonal(HabiticaBaseModel):
    label: str
    achievements: SeasonalAchievements


class BasicAchievements(HabiticaBaseModel):
    streak: AchievementEvent
    perfect: AchievementEvent
    party_up: AchievementEvent
    party_on: AchievementEvent
    joined_guild: AchievementEvent
    royally_loyal: AchievementEvent
    joined_challenge: AchievementEvent
    invited_friend: AchievementEvent
    lost_masterclasser: AchievementEvent
    mind_over_matter: AchievementEvent
    just_add_water: AchievementEvent
    back_to_basics: AchievementEvent
    all_your_base: AchievementEvent
    dust_devil: AchievementEvent
    arid_authority: AchievementEvent
    monster_magus: AchievementEvent
    undead_undertaker: AchievementEvent
    primed_for_painting: AchievementEvent
    pearly_pro: AchievementEvent
    tickled_pink: AchievementEvent
    rosy_outlook: AchievementEvent
    bug_bonanza: AchievementEvent
    bare_necessities: AchievementEvent
    freshwater_friends: AchievementEvent
    good_as_gold: AchievementEvent
    all_that_glitters: AchievementEvent
    bone_collector: AchievementEvent
    skeleton_crew: AchievementEvent
    seeing_red: AchievementEvent
    red_letter_day: AchievementEvent
    legendary_bestiary: AchievementEvent
    seasonal_specialist: AchievementEvent
    violets_are_blue: AchievementEvent
    wild_blue_yonder: AchievementEvent
    domesticated: AchievementEvent
    shady_customer: AchievementEvent
    shade_of_it_all: AchievementEvent
    zodiac_zookeeper: AchievementEvent
    birds_of_a_feather: AchievementEvent
    reptacular_rumble: AchievementEvent
    woodland_wizard: AchievementEvent
    beast_master: AchievementEvent
    mount_master: AchievementEvent
    triad_bingo: AchievementEvent
    healer_ultimate_gear: AchievementEvent
    rogue_ultimate_gear: AchievementEvent
    warrior_ultimate_gear: AchievementEvent
    mage_ultimate_gear: AchievementEvent
    greeting_cards: AchievementEvent
    thankyou_cards: AchievementEvent
    birthday_cards: AchievementEvent
    congrats_cards: AchievementEvent
    getwell_cards: AchievementEvent
    goodluck_cards: AchievementEvent
    rebirth: AchievementEvent


class Basic(HabiticaBaseModel):
    label: str
    achievements: BasicAchievements


class OnboardingAchievements(HabiticaBaseModel):
    created_task: AchievementEvent
    completed_task: AchievementEvent
    hatched_pet: AchievementEvent
    fed_pet: AchievementEvent
    purchased_equipment: AchievementEvent


class Onboarding(HabiticaBaseModel):
    label: str
    achievements: OnboardingAchievements


class Achievement(HabiticaBaseModel):
    basic: Basic
    onboarding: Onboarding
    seasonal: Seasonal
    special: SpecialAchievement


class GetAchievementsResponse(Response):
    data: Achievement
