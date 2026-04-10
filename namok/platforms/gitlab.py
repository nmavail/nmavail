import httpx

from ..config import Config
from .base import BaseChecker


class GitLabChecker(BaseChecker):
    @property
    def name(self) -> str:
        return "GitLab"

    async def check(self, name: str) -> bool | dict:
        # 定义两个检查地址：官网和极狐
        targets = [
            ("GitLab.com", f"https://gitlab.com/api/v4/users?username={name}"),
            ("JiHu GitLab", f"https://jihulab.com/api/v4/users?username={name}")
        ]
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        token = Config().GITLAB_TOKEN
        if token:
            headers["PRIVATE-TOKEN"] = token

        for platform_name, url in targets:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(url, headers=headers, timeout=5.0)
                    if response.status_code == 200:
                        return len(response.json()) == 0
                    elif response.status_code == 403:
                        continue # 尝试下一个地址
                    else:
                        return {"error": f"HTTP {response.status_code}"}
                except httpx.TimeoutException:
                    continue # 超时则尝试下一个地址
                except Exception:
                    continue
        
        return {"error": "Timeout"}
