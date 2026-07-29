from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

DEFAULT_RESOLVERS = (
    "1.1.1.1",
    "1.0.0.1",
    "8.8.8.8",
    "8.8.4.4",
    "9.9.9.9",
    "149.112.112.112",
    "208.67.222.222",
    "208.67.220.220",
)


@dataclass(frozen=True)
class Paths:
    root: Path
    sources: Path
    allowlist: Path
    inactive_cache: Path
    domains_txt: Path
    domains_json: Path

    @classmethod
    def from_root(cls, root: Path) -> Paths:
        root = root.resolve()
        return cls(
            root=root,
            sources=root / "config" / "sources.txt",
            allowlist=root / "allowlist.txt",
            inactive_cache=root / "cache" / "inactive_domains.txt",
            domains_txt=root / "domains.txt",
            domains_json=root / "domains.json",
        )
