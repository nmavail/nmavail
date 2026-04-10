import httpx
from bs4 import BeautifulSoup

from .base import BaseChecker


class BaseUnixChecker(BaseChecker):
    """提供带镜像重试功能的基类"""

    async def _check_urls(
        self, name: str, urls: list[str], is_list: bool = False, is_html: bool = False
    ) -> bool | dict:
        headers = {"User-Agent": "Nmck-Checker/1.0"}
        for url in urls:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(url, headers=headers, timeout=10.0)
                    if response.status_code == 404:
                        return True  # 可用
                    elif response.status_code == 200:
                        # 根据不同类型判断是否真的“存在”
                        if is_list:
                            data = response.json()
                            # AUR RPC 返回 results 列表
                            if isinstance(data, dict) and not data.get("results"):
                                return True
                        elif is_html:
                            # 简单判断 HTML 中是否包含包名（简化逻辑）
                            if name not in response.text:
                                return True
                        else:
                            # JSON API 通常 200 就代表存在
                            pass
                        return False  # 已占用
                except Exception:
                    continue  # 尝试下一个镜像
        return {"error": "Timeout"}


class HomebrewChecker(BaseUnixChecker):
    @property
    def name(self) -> str:
        return "Homebrew"

    async def check(self, name: str) -> bool | dict:
        urls = [
            f"https://formulae.brew.sh/api/formula/{name}.json",
            f"https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/api/formula/{name}.json",
            f"https://raw.githubusercontent.com/Homebrew/homebrew-core/master/Formula/{name[0]}/{name}.rb",
        ]
        headers = {"User-Agent": "Nmck-Checker/1.0"}
        for url in urls:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(url, headers=headers, timeout=10.0)
                    if response.status_code == 404:
                        return True  # 可用
                    elif response.status_code == 200:
                        # 校验 JSON 内容，确保不是错误页
                        try:
                            data = response.json()
                            # Homebrew API 返回的 JSON 通常包含 "name" 字段
                            return not (
                                isinstance(data, dict) and data.get("name") == name
                            )
                        except Exception:
                            continue
                except Exception:
                    continue
        return {"error": "Timeout"}


class AurChecker(BaseUnixChecker):
    @property
    def name(self) -> str:
        return "Arch (AUR)"

    async def check(self, name: str) -> bool | dict:
        urls = [
            f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={name}",
            f"https://mirrors.tuna.tsinghua.edu.cn/aur/rpc/?v=5&type=search&arg={name}",
        ]
        headers = {"User-Agent": "Nmck-Checker/1.0"}
        for url in urls:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(url, headers=headers, timeout=10.0)
                    if response.status_code == 200:
                        data = response.json()
                        # AUR RPC 返回 results 列表
                        return not (isinstance(data, dict) and not data.get("results"))
                except Exception:
                    continue
        return {"error": "Timeout"}


class AptChecker(BaseUnixChecker):
    @property
    def name(self) -> str:
        return "Debian/Ubuntu"

    async def check(self, name: str) -> bool | dict:
        urls = [
            f"https://sources.debian.org/api/src/{name}/",
        ]
        headers = {"User-Agent": "Nmck-Checker/1.0"}
        for url in urls:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(url, headers=headers, timeout=10.0)
                    if response.status_code == 404:
                        return True  # 可用
                    elif response.status_code == 200:
                        # 校验返回内容是否为有效的 JSON 且包含包信息
                        try:
                            data = response.json()
                            # 如果返回的是空列表或没有 versions 字段，通常意味着没找到
                            return not (
                                not data
                                or "versions" not in data
                                or not data["versions"]
                            )
                        except Exception:
                            # 如果解析 JSON 失败（比如返回了 HTML 挑战页），视为查不到
                            return {"error": "Timeout"}
                except Exception:
                    continue
        return {"error": "Timeout"}


class AlpineChecker(BaseUnixChecker):
    @property
    def name(self) -> str:
        return "Alpine Linux"

    async def check(self, name: str) -> bool | dict:
        url = f"https://pkgs.alpinelinux.org/packages?name={name}&branch=edge"
        headers = {"User-Agent": "Nmck-Checker/1.0"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=10.0)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    # 查找是否有实际的包结果表格行
                    # Alpine 的搜索结果在 <tbody> 中，如果没有包会显示 "No matching packages found"
                    if "No matching packages found" in response.text:
                        return True
                    # 或者检查是否有指向具体包的链接
                    package_links = soup.find_all(
                        "a", href=lambda h: h and "/package/" in h
                    )
                    return bool(not package_links)
                return {"error": "Timeout"}
            except Exception:
                return {"error": "Timeout"}
