import httpx

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
                response = await client.get(url, timeout=10.0)
                if response.status_code == 404:
                    return True
                elif response.status_code == 200:
                    return False
                else:
                    return {"error": f"HTTP {response.status_code}"}
            except Exception:
                return {"error": "Timeout/NetErr"}


# 预定义的检查器实例
PYPI_CHECKER = PackageChecker("PyPI", "https://pypi.org/simple/{name}/")
NPM_CHECKER = PackageChecker("NPM", "https://registry.npmjs.org/{name}")
CRATES_CHECKER = PackageChecker("Crates.io", "https://crates.io/api/v1/crates/{name}")
GO_CHECKER = PackageChecker("Go Modules", "https://proxy.golang.org/{name}/@v/list")
