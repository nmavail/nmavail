"""Shared HTTP helpers: proxy normalization and a fault-tolerant client factory.

httpx raises ``ValueError: Unknown scheme for proxy URL`` during
``AsyncClient()`` construction when it picks up an unsupported proxy scheme
from the environment (a very common one being ``socks://``, which httpx does
not understand -- it only supports ``socks5://`` / ``socks5h://``).

Because that failure happens at construction time, before any request is
made, it cannot be caught by the per-checker ``try/except`` blocks. So we
normalize the environment up front and provide a ``http_client()`` factory that
degrades to a direct connection instead of raising.
"""

import importlib.util
import os

import httpx
from rich.console import Console

from .config import DEFAULT_TIMEOUT

# Proxy schemes httpx accepts, mapped from the (invalid) spellings people
# commonly export in their shell profiles.
_SCHEME_ALIASES = {
    "socks": "socks5",
    "socks4": "socks5",
    "socks5h": "socks5h",
}

_SOCKS_SCHEMES = {"socks5", "socks5h"}

# Proxy env vars httpx consults, in its own resolution order (lowercase first).
_ALL_PROXY_VARS = ("all_proxy", "ALL_PROXY")
_PROXY_VARS = (
    *_ALL_PROXY_VARS,
    "http_proxy",
    "HTTP_PROXY",
    "https_proxy",
    "HTTPS_PROXY",
)

_warned = False


def _warn(message: str) -> None:
    """Emit a one-shot warning, consistent with the rich output elsewhere."""
    global _warned
    if _warned:
        return
    _warned = True
    Console(stderr=True).print(f"[yellow]nmavail: {message}[/yellow]")


def _has_socks_support() -> bool:
    """httpx needs the ``socksio`` extra to speak SOCKS."""
    try:
        return importlib.util.find_spec("socksio") is not None
    except (ImportError, ValueError):
        return False


def normalize_proxy_env() -> None:
    """Rewrite unusable proxy environment variables in place.

    - ``socks://`` / ``socks4://`` are remapped to a scheme httpx accepts.
    - If SOCKS support is unavailable (no ``socksio``), unusable variables are
      dropped so httpx falls back to the remaining usable proxy (or a direct
      connection) instead of failing.

    Mutating the environment (rather than passing ``proxy=`` ourselves) keeps
    httpx's native handling of ``NO_PROXY`` and per-scheme variables intact.
    """
    socks_ok = _has_socks_support()
    dropped: list[str] = []

    for var in _PROXY_VARS:
        raw = os.environ.get(var)
        if not raw:
            continue

        url = raw.strip()
        scheme, sep, rest = url.partition("://")
        if not sep:
            continue

        fixed_scheme = _SCHEME_ALIASES.get(scheme.lower())
        if not fixed_scheme:
            continue

        if fixed_scheme in _SOCKS_SCHEMES and not socks_ok:
            # Nothing httpx can do with this one.
            dropped.append(var)
            continue

        os.environ[var] = f"{fixed_scheme}://{rest}"

    for var in dropped:
        _warn(
            f"{var}={os.environ[var]!r} needs the 'socksio' package, which is "
            f"not installed; ignoring it. Install with: pip install 'httpx[socks]'"
        )
        os.environ.pop(var, None)


def http_client(**kwargs) -> httpx.AsyncClient:
    """Build an ``httpx.AsyncClient`` that never dies on proxy configuration.

    Any keyword accepted by ``httpx.AsyncClient`` may be passed through. On a
    proxy-related construction failure we retry once with ``trust_env=False``
    so a misconfigured proxy degrades to a direct connection rather than
    aborting every check.
    """
    normalize_proxy_env()
    kwargs.setdefault("timeout", DEFAULT_TIMEOUT)

    try:
        return httpx.AsyncClient(**kwargs)
    except ValueError as exc:
        _warn(f"Invalid proxy configuration ({exc}); ignoring proxies.")
        return httpx.AsyncClient(trust_env=False, **kwargs)
