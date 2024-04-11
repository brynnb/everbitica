import requests

import habitica.error
from habitica.consts import ClassType, EquipType
from habitica import error
from habitica.common import HabiticaEndpointsProcessor
from habitica.common_model import EmptyResponse, Response, ResponseWithMessage
from habitica.user_model import GetUserInfoResponse, HatchPetResponse, SleepWakeUpResponse


class UserClient(HabiticaEndpointsProcessor):
    @staticmethod
    def _map_error(data, schema) -> Response:
        if data["success"] is False:
            e = getattr(error, f"{data['error']}Error")
            raise e(data["message"])
        return schema.parse_obj(data)

    def allocate_point(self, stat: str):
        url = self._build_url("user/allocate")
        params = {"stat": stat}
        response = requests.post(url=url, params=params, headers=self._get_auth_headers())
        return self._map_error(response.json(), Response)
        # TODO: Choose schema

    def allocate_all(self):
        pass

    def allocate_bulk(self, stats):
        pass

    def block_user(self, user_id):
        pass

    def buy_health_potion(self):
        pass

    def buy_mystery_set(self, item_key):
        pass

    def buy_gear(self, item_key):
        pass

    def buy_quest(self, item_key):
        pass

    def buy_armoire(self):
        pass

    def buy(self, item_key):
        pass

    def buy_special_spell(self, item_key):
        pass

    def cast(self, spell: str, target_id: str = None):
        pass

    def change_class(self, new_class: str):
        if new_class not in list(ClassType):
            raise habitica.error.BadRequestError(f"Unknown class requested: {new_class}")
        url = self._build_url("user/change-class")
        response = requests.post(url=url, headers=self._get_auth_headers(), params={"class": new_class})
        return self._map_error(response.json(), Response)
        # TODO: Choose schema

    def delete_message(self, message_id):
        url = self._build_url(f"user/messages/{message_id}")
        response = requests.delete(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), Response)
        # TODO: Choose schema

    def delete_all_messages(self):
        url = self._build_url("user/messages")
        response = requests.delete(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), EmptyResponse)

    def disable_classes(self):
        url = self._build_url("user/disable-classes")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), Response)
        # TODO: Choose schema

    def equip_or_unequip_item(self, equip_type: str, key: str):
        if equip_type not in list(EquipType):
            raise habitica.error.BadRequestError(f"Unknown equip type requested: {equip_type}")
        url = self._build_url(f"user/equip/{equip_type}/{key}")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), Response)
        # TODO: Choose schema

    def feed_pet(self, pet, food, amount: int = 1):
        """
        :param pet:
        :param food:
        :param amount: The amount of food to feed. Note: Pet can eat 50 units.
        Preferred food offers 5 units per food, other food 2 units.
        :return:
        """
        url = self._build_url(f"user/feed/{pet}/{food}")
        response = requests.post(url=url, headers=self._get_auth_headers(), params={"amount": amount})
        return self._map_error(response.json(), Response)
        # TODO: Choose schema

    def get_equipment_in_shop(self):
        url = self._build_url("user/inventory/buy")
        response = requests.get(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), Response)
        # TODO: Choose schema

    def get_user_info(self, user_fields: str = None):
        url = self._build_url("user")
        params = {}
        if user_fields is not None:
            params["userFields"] = user_fields
        response = requests.get(url=url, headers=self._get_auth_headers(), params=params)
        return self._map_error(response.json(), GetUserInfoResponse)

    def hatch_pet(self, egg, potion):
        url = self._build_url(f"user/hatch/{egg}/{potion}")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), HatchPetResponse)

    def sleep_or_wake_up(self):
        url = self._build_url("user/sleep")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), SleepWakeUpResponse)

    def mark_direct_messages_read(self):
        url = self._build_url("user/mark-pms-read")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), Response)
        # TODO: Choose schema

    def open_mystery_item(self):
        url = self._build_url("user/open-mystery-item")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), Response)
        # TODO: Choose schema

    def purchase_gem_or_gemable(self, purchase_type: str, key: str):
        url = self._build_url(f"user/purchase/{purchase_type}/{key}")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), Response)
        # TODO: Choose schema

    def purchase_hourglassable(self, purchase_type: str, key: str, quantity: int = 1):
        url = self._build_url(f"user/purchase-hourglass/{purchase_type}/{key}")
        data = {"quantity": quantity}
        response = requests.post(url=url, headers=self._get_auth_headers(), json=data)
        return self._map_error(response.json(), Response)
        # TODO: Choose schema

    def read_card(self, card_type: str):
        url = self._build_url(f"user/read-card/{card_type}")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), Response)
        # TODO: Choose schema

    def release_mounts(self):
        url = self._build_url("user/release-mounts")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), Response)
        # TODO: Choose schema

    def release_both(self):
        url = self._build_url("user/release-both")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), Response)
        # TODO: Choose schema

    def reroll(self):
        url = self._build_url("user/reroll")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), Response)
        # TODO: Choose schema

    def reset(self):
        url = self._build_url("user/reset")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), Response)
        # TODO: Choose schema

    def revive(self):
        url = self._build_url("user/revive")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), Response)
        # TODO: Choose schema

    def sell_gold_sellable(self, item_type, key):
        url = self._build_url(f"user/sell/{item_type}/{key}")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), Response)
        # TODO: Choose schema

    def set_custom_day_start(self, day_start: int):
        url = self._build_url("user/custom-day-start")
        data = {"dayStart": day_start}
        response = requests.post(url=url, headers=self._get_auth_headers(), json=data)
        return self._map_error(response.json(), ResponseWithMessage)

    def do_rebirth(self):
        url = self._build_url("user/rebirth")
        response = requests.post(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), Response)
        # TODO: Choose schema
