import httpx

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
            f"https://raw.githubusercontent.com/Homebrew/homebrew-core/master/Formula/{name[0]}/{name}.rb",
        ]
        return await self._check_urls(name, urls)


class AurChecker(BaseUnixChecker):
    @property
    def name(self) -> str:
        return "Arch (AUR)"

    async def check(self, name: str) -> bool | dict:
        urls = [
            f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={name}",
            f"https://mirrors.tuna.tsinghua.edu.cn/aur/rpc/?v=5&type=search&arg={name}",
        ]
        return await self._check_urls(name, urls, is_list=True)


class AptChecker(BaseUnixChecker):
    @property
    def name(self) -> str:
        return "Debian/Ubuntu"

    async def check(self, name: str) -> bool | dict:
        urls = [
            f"https://sources.debian.org/api/src/{name}/",
        ]
        return await self._check_urls(name, urls)


class AlpineChecker(BaseUnixChecker):
    @property
    def name(self) -> str:
        return "Alpine Linux"

    async def check(self, name: str) -> bool | dict:
        urls = [
            f"https://pkgs.alpinelinux.org/packages?name={name}&branch=edge",
            "https://mirrors.tuna.tsinghua.edu.cn/alpine/edge/main/x86_64/",
        ]
        return await self._check_urls(name, urls, is_html=True)
