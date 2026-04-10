import httpx

from ..config import Config
from .base import BaseChecker


class GitLabChecker(BaseChecker):
    @property
    def name(self) -> str:
        return "GitLab"

    async def check(self, name: str) -> bool | dict:
        url = f"https://gitlab.com/api/v4/users?username={name}"
        headers = {}
        if Config.GITLAB_TOKEN:
            headers["PRIVATE-TOKEN"] = Config.GITLAB_TOKEN

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=10.0)
                if response.status_code == 200:
                    # 如果返回空列表，说明用户不存在（可用）
                    return len(response.json()) == 0
                else:
                    return {"error": f"HTTP {response.status_code}"}
            except Exception:
                return {"error": "Timeout/NetErr"}
