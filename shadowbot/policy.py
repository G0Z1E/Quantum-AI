from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

# This policy is intentionally strict to keep ShadowBot defensive-only.
DENY_TOKENS = [
    "nc", "netcat", "ncat",
    "bash -i", "sh -i",
    "socat",
    "msfconsole", "meterpreter",
    "powershell -enc", "base64",
    "mimikatz",
    "hydra", "john", "hashcat",
    "ftp", "telnet",
    "curl http", "wget http",
    "python -c", "perl -e",
    "rm -rf", ":(){", "dd if=",
]

@dataclass
class CommandPolicy:
    allowed_prefixes: List[str] = field(default_factory=lambda: [
        "whoami",
        "uname",
        "uptime",
        "df",
        "free",
        "ip",
        "ss",
        "ping",
        "traceroute",
        "dig",
        "nslookup",
        "journalctl",
        "systemctl status",
        "nmap",  # allowed but can be restricted further by targets in config
    ])
    deny_tokens: List[str] = field(default_factory=lambda: DENY_TOKENS)

    def is_allowed(self, cmd: str) -> bool:
        c = cmd.strip().lower()

        # deny-list tokens
        for token in self.deny_tokens:
            if token in c:
                return False

        # allow-list prefixes
        for pref in self.allowed_prefixes:
            if c.startswith(pref):
                return True

        return False
