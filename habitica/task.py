import requests

import habitica.error
from habitica.consts import DirectionType, TaskType
from habitica import error
from habitica.common import HabiticaEndpointsProcessor
from habitica.common_model import EmptyResponse
from habitica.group_model import Response
from habitica.task_model import (
    TaskPositionsResponse,
    TaskResponse,
    TaskScoreResponse,
    TasksResponse,
)


class TaskClient(HabiticaEndpointsProcessor):
    @staticmethod
    def _map_error(data, schema) -> Response:
        if data["success"] is False:
            e = getattr(error, f"{data['error']}Error")
            raise e(data["message"])
        return schema.parse_obj(data)

    def create(self, data):
        url = self._build_url("tasks/user")
        response = requests.post(url, headers=self._get_auth_headers(), json=data)
        return self._map_error(response.json(), TaskResponse)

    def delete(self, task_id):
        url = self._build_url(f"tasks/{task_id}")
        response = requests.delete(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), EmptyResponse)

    def get_info(self, task_id):
        url = self._build_url(f"tasks/{task_id}")
        response = requests.get(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), TaskResponse)

    def get_all(self, task_type=None, due_date=None):
        url = self._build_url("tasks/user")
        params = {}
        if task_type is not None:
            if task_type not in list(TaskType):
                raise habitica.error.BadRequestError(f"No such task type: {task_type}")
            params["task_type"] = f"{task_type}s"
        if due_date is not None:
            params["due_date"] = due_date
        response = requests.get(url, headers=self._get_auth_headers(), params=params)
        return self._map_error(response.json(), TasksResponse)

    def move_new_position(self, task_id, position):
        url = self._build_url(f"tasks/{task_id}/move/to/{position}")
        response = requests.post(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), TaskPositionsResponse)

    def score(self, task_id, direction):
        """
        Only valid for type "habit"

        If direction is "up", enables the "+" under "Directions/Action" for "Good habits".
        If direction is "down", enables the "-" under "Directions/Action" for "Bad habits".
        """
        if direction not in list(DirectionType):
            raise habitica.error.BadRequestError(f"No such direction type: {direction}")
        url = self._build_url(f"tasks/{task_id}/score/{direction}")
        response = requests.post(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), TaskScoreResponse)

    def update(self, task_id, data):
        url = self._build_url(f"tasks/{task_id}")
        response = requests.put(url, headers=self._get_auth_headers(), json=data)
        return self._map_error(response.json(), TaskResponse)

    def clear_completed(self):
        url = self._build_url("tasks/clearCompletedTodos")
        response = requests.post(url, headers=self._get_auth_headers())
        return self._map_error(response.json(), EmptyResponse)

    # Tags
    def add_tag(self, task_id: str, tag_if: str):
        pass

    def delete_tag(self, task_id, tag_id):
        pass

    # Checklists
    def add_checklist_item(self, task_id, text, completed):
        pass

    def delete_checklist_item(self, task_id, item_id):
        pass

    def update_checklist_item(self, task_id, item_id, text, completed):
        pass

    def score_checklist_item(self, task_id, item_id, data):
        pass

    # Challenge
    def create_new_challenge_task(self, challenge_id, data):
        pass

    def get_challenge_tasks(self, challenge_id):
        pass

    def unlink_challenge_task(self, task_id, keep):
        pass

    def unlink_all_challenge_tasks(self, challenge_id, keep):
        pass

    # Group
    def assign_group_task_to_user(self, task_id, user_id):
        pass

    def create_new_group_task(self, group_id, data):
        pass

    def get_group_tasks(self, group_id):
        pass

    def unassign_user(self, task_id, user_id):
        pass
