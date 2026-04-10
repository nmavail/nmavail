import httpx

from ..config import DEFAULT_TIMEOUT, Config
from .base import BaseChecker


class GitHubChecker(BaseChecker):
    @property
    def name(self) -> str:
        return "GitHub (User/Org)"

    async def check(self, name: str) -> bool | dict:
        url = f"https://api.github.com/users/{name}"
        headers = {}
        token = Config().github_token
        if token:
            headers["Authorization"] = f"token {token}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url, headers=headers, timeout=DEFAULT_TIMEOUT
                )
                if response.status_code == 404:
                    return True  # User doesn't exist, available
                elif response.status_code == 200:
                    return False  # User exists, taken
                elif response.status_code == 401:
                    return {"error": "Auth Failed"}
                else:
                    return {"error": f"HTTP {response.status_code}"}
            except httpx.TimeoutException:
                return {"error": "Timeout"}
            except httpx.RequestError as e:
                return {"error": f"Network: {type(e).__name__}"}


class GitHubRepoChecker(BaseChecker):
    @property
    def name(self) -> str:
        return "GitHub (Repo Search)"

    async def check(self, name: str) -> dict:
        """Return a dict with available status and top_stars count"""
        # Try exact match first, fallback to general search
        url = f"https://api.github.com/search/repositories?q={name}+in:name&per_page=1&sort=stars&order=desc"
        headers = {"Accept": "application/vnd.github.v3+json"}
        token = Config().github_token
        if token:
            headers["Authorization"] = f"token {token}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url, headers=headers, timeout=DEFAULT_TIMEOUT
                )
                if response.status_code == 200:
                    data = response.json()
                    total_count = data.get("total_count", 0)
                    items = data.get("items", [])
                    if items:
                        top_stars = items[0].get("stargazers_count", 0)
                        return {
                            "available": False,
                            "top_stars": top_stars,
                            "total_count": total_count,
                        }
                    else:
                        return {"available": True, "top_stars": None, "total_count": 0}
                elif response.status_code == 401:
                    return {"error": "Auth Failed"}
                else:
                    return {"error": f"HTTP {response.status_code}"}
            except httpx.TimeoutException:
                return {"error": "Timeout"}
            except httpx.RequestError as e:
                return {"error": f"Network: {type(e).__name__}"}
