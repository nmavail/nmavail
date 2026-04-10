import httpx

from ..config import DEFAULT_TIMEOUT, Config
from .base import BaseChecker


class GitLabChecker(BaseChecker):
    @property
    def name(self) -> str:
        return "User/Group"

    async def check(self, name: str) -> bool | dict:
        # Always use GitLab.com
        url = f"https://gitlab.com/api/v4/users?username={name}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        token = Config().gitlab_token
        if token:
            headers["PRIVATE-TOKEN"] = token

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url, headers=headers, timeout=DEFAULT_TIMEOUT
                )
                if response.status_code == 200:
                    return len(response.json()) == 0
                elif response.status_code == 403:
                    return {"error": "Auth Failed"}
                else:
                    return {"error": f"HTTP {response.status_code}"}
            except httpx.TimeoutException:
                return {"error": "Timeout"}
            except httpx.RequestError as e:
                return {"error": f"Network: {type(e).__name__}"}


class GitLabRepoChecker(BaseChecker):
    @property
    def name(self) -> str:
        return "Repo Search"

    async def check(self, name: str) -> dict:
        """Search for matching repos on GitLab and return star count info"""
        # Always use GitLab.com
        base_url = "https://gitlab.com/api/v4/projects"

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
        }
        token = Config().gitlab_token
        if token:
            headers["PRIVATE-TOKEN"] = token

        try:
            async with httpx.AsyncClient() as client:
                # Only fetch 1 page (100 results) to avoid slow queries
                params = {
                    "search": name,
                    "per_page": 100,  # Max allowed
                    "page": 1,
                }
                response = await client.get(
                    base_url,
                    headers=headers,
                    params=params,
                    timeout=DEFAULT_TIMEOUT,
                )
                if response.status_code != 200:
                    return {"error": f"HTTP {response.status_code}"}

                projects = response.json()
                if not projects:
                    return {"available": True, "top_stars": None, "total_count": 0}

                # Find the project with highest stars from first page
                top_project = max(projects, key=lambda p: p.get("star_count", 0))
                top_stars = top_project.get("star_count", 0)
                total_count = len(projects)

                # Check if there are more pages
                next_page = response.headers.get("x-next-page")
                has_more = next_page is not None

                # If there are more pages, indicate with "+" and ">="
                if has_more:
                    total_count = f"{total_count}+"

                return {
                    "available": False,
                    "top_stars": top_stars,
                    "total_count": total_count,
                    "has_more": has_more,
                }
        except httpx.TimeoutException:
            return {"error": "Timeout"}
        except httpx.RequestError as e:
            return {"error": f"Network: {type(e).__name__}"}
        except Exception:
            return {"error": "Timeout"}
