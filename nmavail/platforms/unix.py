import httpx
from bs4 import BeautifulSoup

from ..config import DEFAULT_TIMEOUT
from .base import BaseChecker


class BaseUnixChecker(BaseChecker):
    """Base class with mirror retry functionality"""

    async def _check_urls(
        self, name: str, urls: list[str], is_list: bool = False, is_html: bool = False
    ) -> bool | dict:
        headers = {"User-Agent": "Nmck-Checker/1.0"}
        for url in urls:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(
                        url, headers=headers, timeout=DEFAULT_TIMEOUT
                    )
                    if response.status_code == 404:
                        return True  # Available
                    elif response.status_code == 200:
                        # Check existence based on type
                        if is_list:
                            data = response.json()
                            # AUR RPC returns results list
                            if isinstance(data, dict) and not data.get("results"):
                                return True
                        elif is_html:
                            # Simple check if package name exists in HTML
                            if name not in response.text:
                                return True
                        else:
                            # JSON API usually means exists if 200
                            pass
                        return False  # Taken
                except httpx.TimeoutException:
                    continue  # Try next mirror
                except httpx.RequestError:
                    continue  # Try next mirror
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
                    response = await client.get(
                        url, headers=headers, timeout=DEFAULT_TIMEOUT
                    )
                    if response.status_code == 404:
                        return True  # Available
                    elif response.status_code == 200:
                        # Validate JSON content to ensure it's not an error page
                        try:
                            data = response.json()
                            # Homebrew API usually returns JSON with "name" field
                            return not (
                                isinstance(data, dict) and data.get("name") == name
                            )
                        except httpx.RequestError:
                            continue
                except httpx.TimeoutException:
                    continue
                except httpx.RequestError:
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
                    response = await client.get(
                        url, headers=headers, timeout=DEFAULT_TIMEOUT
                    )
                    if response.status_code == 200:
                        data = response.json()
                        # AUR RPC returns results list
                        # Check if response is an error
                        if "error" in data:
                            # "Too many package results" means package exists
                            if "Too many" in data["error"]:
                                return False  # Package exists, taken
                            return {"error": data["error"]}

                        results = data.get("results", [])
                        # Check for exact name match
                        has_exact_match = any(
                            pkg.get("Name") == name for pkg in results
                        )
                        return not has_exact_match
                except httpx.TimeoutException:
                    continue
                except httpx.RequestError:
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
                    response = await client.get(
                        url, headers=headers, timeout=DEFAULT_TIMEOUT
                    )
                    if response.status_code == 200:
                        # Debian API returns 200 even for not found, but with error in JSON
                        try:
                            data = response.json()
                            # Check if response contains error
                            if "error" in data:
                                return True  # Package not found, available
                            # If has versions or is a valid package response
                            return not ("versions" in data and bool(data["versions"]))
                        except httpx.RequestError:
                            # If JSON parsing fails, treat as error
                            return {"error": "Timeout"}
                except httpx.TimeoutException:
                    continue
                except httpx.RequestError:
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
                response = await client.get(
                    url, headers=headers, timeout=DEFAULT_TIMEOUT
                )
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    # Look for actual package result table rows
                    # Alpine search results are in <tbody>, shows "No matching packages found" if no packages
                    if "No matching packages found" in response.text:
                        return True
                    # Or check for links to specific packages
                    package_links = soup.find_all(
                        "a", href=lambda h: h and "/package/" in h
                    )
                    return bool(not package_links)
                return {"error": "Timeout"}
            except httpx.TimeoutException:
                return {"error": "Timeout"}
            except httpx.RequestError:
                return {"error": "Timeout"}
