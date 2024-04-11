import requests

from habitica import error
from habitica.common import HabiticaEndpointsProcessor
from habitica.common_model import EmptyResponse
from habitica.group_model import Response
from habitica.tag_model import TagResponse, TagsListResponse


class TagClient(HabiticaEndpointsProcessor):
    @staticmethod
    def _map_error(data, schema) -> Response:
        if data["success"] is False:
            e = getattr(error, f"{data['error']}Error")
            raise e(data["message"])
        return schema.parse_obj(data)

    def create(self, name: str):
        url = self._build_url("tags")
        data = {"name": name}
        response = requests.post(url=url, headers=self._get_auth_headers(), json=data)
        return self._map_error(response.json(), TagsListResponse)

    def delete(self, tag_id: str):
        url = self._build_url(f"tags/{tag_id}")
        response = requests.delete(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), EmptyResponse)

    def get(self, tag_id: str):
        url = self._build_url(f"tags/{tag_id}")
        response = requests.get(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), TagResponse)

    def update(self, tag_id: str, name: str):
        url = self._build_url(f"tags/{tag_id}")
        data = {"name": name}
        response = requests.put(url=url, headers=self._get_auth_headers(), json=data)
        return self._map_error(response.json(), TagResponse)

    def get_all(self):
        url = self._build_url("tags")
        response = requests.get(url=url, headers=self._get_auth_headers())
        return self._map_error(response.json(), TagsListResponse)

    def move_new_position(self, tag_id: str, position: int):
        """
        Stupid question why interface of task.move_new_position and tag.move_new_position are so different?
        """
        url = self._build_url("reorder-tags")
        data = {"tagId": tag_id, "to": position}
        response = requests.post(url=url, headers=self._get_auth_headers(), json=data)
        return self._map_error(response.json(), EmptyResponse)
