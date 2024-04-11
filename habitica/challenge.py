import requests

import habitica.error
from habitica.consts import KeepType
from habitica import error
from habitica.common import HabiticaEndpointsProcessor
from habitica.challenge_model import ChallengeResponse, ChallengesListResponse
from habitica.common_model import EmptyResponse, Response


class ChallengeClient(HabiticaEndpointsProcessor):
    @staticmethod
    def _map_error(data, schema) -> Response:
        if data["success"] is False:
            e = getattr(error, f"{data['error']}Error")
            raise e(data["message"])
        return schema.parse_obj(data)

    def clone(self, challenge_id: str):
        url = self._build_url(f"challenges/{challenge_id}/clone")
        response = requests.post(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), ChallengeResponse)

    def create(self, data: dict):
        url = self._build_url("challenges")
        response = requests.post(url, headers=self._get_auth_headers(), json=data)
        return self._map_error(response.json(), ChallengeResponse)

    def delete(self, challenge_id: str):
        url = self._build_url(f"challenges/{challenge_id}")
        response = requests.delete(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), EmptyResponse)

    def export_csv(self, challenge_id: str):
        url = self._build_url(f"challenges/{challenge_id}/export/csv")
        requests.get(url, headers=self._get_auth_headers())
        # TODO what about response?

    def get(self, challenge_id: str):
        url = self._build_url(f"challenges/{challenge_id}")
        response = requests.get(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), ChallengeResponse)

    def get_challenges_for_a_group(self, group_id: str = "party"):
        # strange route, maybe should be moved in groups client
        url = self._build_url(f"challenges/groups/{group_id}")
        response = requests.get(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), ChallengesListResponse)

    def get_all(self, page=0, member=None, owned=None, search=None, categories=None):
        url = self._build_url("challenges/user")
        params = {"page": page}
        if member is not None:
            params["member"] = member
        if owned is not None:
            params["owned"] = owned
        if search is not None:
            params["search"] = search
        if categories is not None:
            params["categories"] = categories
        response = requests.get(url, headers=self._get_auth_headers(), params=params)
        return self._map_error(response.json(), ChallengesListResponse)

    def join(self, challenge_id: str):
        url = self._build_url(f"challenges/{challenge_id}/join")
        response = requests.post(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), ChallengeResponse)

    def leave(self, challenge_id: str, keep: str = None):
        url = self._build_url(f"challenges/{challenge_id}/leave")
        if keep is not None:
            if keep not in list(KeepType):
                raise habitica.error.BadRequestError(f"No such keep type: {keep}")
            data = {"keep": keep}
        response = requests.post(url, headers=self._get_auth_headers(), json=data)
        return self._map_error(response.json(), EmptyResponse)

    def select_winner(self, challenge_id: str, winner_id: str):
        url = self._build_url(f"/challenges/{challenge_id}/selectWinner/{winner_id}")
        response = requests.post(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), EmptyResponse)

    def get_challenge_member_progress(self, challenge_id: str, member_id: str):
        url = self._build_url(f"challenges/{challenge_id}/members/{member_id}")
        response = requests.get(url=url, headers=self._get_auth_headers())
        # TODO: Choose schema
        return self._map_error(response.json(), Response)

    def get_challenge_members(
        self,
        challenge_id: str,
        last_id: str = None,
        limit: int = 30,
        include_tasks: bool = False,
        include_all_public_fields: bool = False,
    ):
        url = self._build_url(f"challenges/{challenge_id}/members")
        params = {"limit": limit, "includeTasks": include_tasks, "includeAllPublicFields": include_all_public_fields}
        if last_id:
            params["lastId"] = last_id
        response = requests.get(url=url, headers=self._get_auth_headers(), params=params)
        # TODO: Choose schema
        return self._map_error(response.json(), Response)

    def update(
        self,
        challenge_id: str,
        name: str = None,
        summary: str = None,
        description: str = None,
    ):
        data = {}
        if name is not None:
            data["name"] = name
        if summary is not None:
            data["summary"] = summary
        if description is not None:
            data["description"] = description
        url = self._build_url(f"challenges/{challenge_id}")
        response = requests.put(url, headers=self._get_auth_headers(), json=data)
        return self._map_error(response.json(), ChallengeResponse)
