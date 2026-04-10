import httpx

from ..config import Config
from .base import BaseChecker


class GitHubChecker(BaseChecker):
    @property
    def name(self) -> str:
        return "GitHub (User/Org)"

    async def check(self, name: str) -> bool | dict:
        url = f"https://api.github.com/users/{name}"
        headers = {}
        token = Config().GITHUB_TOKEN
        if token:
            headers["Authorization"] = f"token {token}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=15.0)
                if response.status_code == 404:
                    return True  # 用户不存在，可用
                elif response.status_code == 200:
                    return False  # 用户存在，已占用
                elif response.status_code == 401:
                    return {"error": "Auth Failed"}
                else:
                    return {"error": f"HTTP {response.status_code}"}
            except Exception:
                return {"error": "Timeout/NetErr"}


class GitHubRepoChecker(BaseChecker):
    @property
    def name(self) -> str:
        return "GitHub (Repo Search)"

    async def check(self, name: str) -> dict:
        """返回一个字典，包含 available 状态和 top_stars 数量"""
        # 尝试精确匹配，如果不行则回退到普通搜索
        url = f"https://api.github.com/search/repositories?q={name}+in:name&per_page=1&sort=stars&order=desc"
        headers = {"Accept": "application/vnd.github.v3+json"}
        token = Config().GITHUB_TOKEN
        if token:
            headers["Authorization"] = f"token {token}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=15.0)
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
            except Exception:
                return {"error": "Timeout/NetErr"}
