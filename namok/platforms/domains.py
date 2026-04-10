import asyncio
import logging

import dns.resolver
import whois

from .base import BaseChecker

# 屏蔽 whois 库的 socket 报错日志
logging.getLogger("whois").setLevel(logging.CRITICAL)

# 主流域名后缀列表
POPULAR_TLDS = [
    "com",
    "org",
    "net",
    "io",
    "co",
    "dev",
    "app",
    "xyz",
    "ai",
    "me",
    "cn",
    "tv",
    "ly",
    "it",
]


class DomainChecker(BaseChecker):
    def __init__(self, tld: str):
        self._tld = tld

    @property
    def name(self) -> str:
        return f"Domain ({self._tld})"

    async def check(self, name: str) -> bool:
        domain = f"{name}.{self._tld}"
        loop = asyncio.get_event_loop()

        # 1. Check WHOIS
        try:
            w = await loop.run_in_executor(None, whois.whois, domain)
            if w.domain_name:
                return False
        except Exception:
            pass

        # 2. Check DNS
        try:
            answers = await loop.run_in_executor(
                None, dns.resolver.resolve, domain, "A"
            )
            if answers:
                return False
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            return True
        except Exception:
            return True

        return True
