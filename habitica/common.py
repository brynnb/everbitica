from urllib.parse import urljoin


class HabiticaEndpointsProcessor:
    base_url = "https://habitica.com/api/v3/"

    def _get_auth_headers(self) -> dict:
        return {
            "x-api-user": self.user_id,
            "x-api-key": self.token,
            "x-client": f"{self.user_id}-python-api",
        }

    def _build_url(self, relative_url):
        return urljoin(self.base_url, relative_url)

    def __init__(self, user_id: str, token: str) -> None:
        self.user_id = user_id
        self.token = token
 