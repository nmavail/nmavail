import asyncio
import logging

import dns.resolver
import whois

from .base import BaseChecker

# Suppress socket error logs from whois library
logging.getLogger("whois").setLevel(logging.CRITICAL)

# Popular TLD list
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

        # Try WHOIS check with retry
        for attempt in range(2):  # Retry once if fails
            try:
                w = await loop.run_in_executor(None, whois.whois, domain)

                # Check if domain exists by verifying status field
                # Most TLDs return status for existing domains, None/empty for non-existing
                # .ly specifically returns domain_name even for non-existing, but status is None
                return not bool(w.status)
            except Exception:
                if attempt == 0:
                    await asyncio.sleep(0.5)  # Wait before retry
                # On second attempt, fall through to DNS check

        # 2. Check DNS as fallback
        try:
            answers = await loop.run_in_executor(
                None, dns.resolver.resolve, domain, "A"
            )
            if answers:
                return False
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            return True
        except Exception:
            # DNS query failed for other reasons (timeout, network, etc.)
            return True

        return True
