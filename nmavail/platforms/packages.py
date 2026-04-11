import httpx

from ..config import DEFAULT_TIMEOUT
from .base import BaseChecker


class PackageChecker(BaseChecker):
    def __init__(self, platform_name: str, url_template: str):
        self._platform_name = platform_name
        self._url_template = url_template

    @property
    def name(self) -> str:
        return self._platform_name

    async def check(self, name: str) -> bool | dict:
        url = self._url_template.format(name=name)
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=DEFAULT_TIMEOUT)
                if response.status_code == 404:
                    return True
                elif response.status_code == 200:
                    return False
                else:
                    return {"error": f"HTTP {response.status_code}"}
            except httpx.TimeoutException:
                return {"error": "Timeout"}
            except httpx.RequestError as e:
                # Network errors, DNS failures, connection refused, etc.
                return {"error": f"Network: {type(e).__name__}"}


# Predefined checker instances
PYPI_CHECKER = PackageChecker("PyPI", "https://pypi.org/simple/{name}/")
NPM_CHECKER = PackageChecker("NPM", "https://registry.npmjs.org/{name}")
CRATES_CHECKER = PackageChecker("Crates.io", "https://crates.io/api/v1/crates/{name}")
GO_CHECKER = PackageChecker("Go Modules", "https://proxy.golang.org/{name}/@v/list")
