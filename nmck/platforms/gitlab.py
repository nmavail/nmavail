import httpx
import urllib.parse

from ..config import Config
from .base import BaseChecker


class GitLabChecker(BaseChecker):
    @property
    def name(self) -> str:
        return "User/Group"

    async def check(self, name: str) -> bool | dict:
        # 根据 Token 情况选择数据源
        token = Config().GITLAB_TOKEN
        if token:
            # 有 Token 时使用 GitLab.com（功能更完整）
            url = f"https://gitlab.com/api/v4/users?username={name}"
        else:
            # 无 Token 时使用极狐（国内更稳定）
            url = f"https://jihulab.com/api/v4/users?username={name}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        if token:
            headers["PRIVATE-TOKEN"] = token

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=8.0)
                if response.status_code == 200:
                    return len(response.json()) == 0
                elif response.status_code == 403:
                    return {"error": "Auth Failed"}
                else:
                    return {"error": f"HTTP {response.status_code}"}
            except httpx.TimeoutException:
                return {"error": "Timeout"}
            except Exception:
                return {"error": "Timeout"}


class GitLabRepoChecker(BaseChecker):
    @property
    def name(self) -> str:
        return "Repo Search"

    async def check(self, name: str) -> dict:
        """搜索 GitLab 上的同名项目并返回星数信息"""
        # 根据 Token 情况选择数据源
        token = Config().GITLAB_TOKEN
        if token:
            # 有 Token 时使用 GitLab.com（功能更完整）
            base_url = "https://gitlab.com/api/v4/projects"
        else:
            # 无 Token 时使用极狐（国内更稳定）
            base_url = "https://jihulab.com/api/v4/projects"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }
        if token:
            headers["PRIVATE-TOKEN"] = token

        try:
            async with httpx.AsyncClient() as client:
                # GitLab API 不支持 order_by=stars，需要获取多个结果后手动找最高星数
                params = {
                    "search": name,
                    "per_page": 20,  # 获取多一点结果来找到最高星的
                }
                response = await client.get(base_url, headers=headers, params=params, timeout=10.0)
                if response.status_code == 200:
                    projects = response.json()
                    if projects:
                        # 手动找出星数最多的项目
                        top_project = max(projects, key=lambda p: p.get("star_count", 0))
                        top_stars = top_project.get("star_count", 0)
                        # 尝试从 Response Headers 获取总数量
                        # GitLab API 会在 header 中返回 x-total (需要认证) 或 x-page 等分页信息
                        total_count = response.headers.get("x-total")
                        if total_count is None:
                            # 如果没有返回总数，说明需要认证或 API 限制
                            # 使用当前页数量作为近似值
                            total_count = len(projects)
                        else:
                            total_count = int(total_count)
                        return {
                            "available": False,
                            "top_stars": top_stars,
                            "total_count": total_count
                        }
                    else:
                        return {"available": True, "top_stars": None, "total_count": 0}
                elif response.status_code == 400:
                    return {"error": f"HTTP {response.status_code}"}
                elif response.status_code in (403, 429):
                    return {"error": "Auth Failed"}
                else:
                    return {"error": f"HTTP {response.status_code}"}
        except httpx.TimeoutException:
            return {"error": "Timeout"}
        except Exception:
            return {"error": "Timeout"}
