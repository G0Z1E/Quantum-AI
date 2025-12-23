from __future__ import annotations
import platform
import socket
import time
from typing import Dict, Any
import subprocess

def _run(cmd: list[str], timeout: int = 10) -> str:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
        out = (p.stdout or "").strip()
        err = (p.stderr or "").strip()
        return out if out else err
    except Exception as e:
        return f"ERROR: {e}"

def host_snapshot() -> Dict[str, Any]:
    return {
        "ts": int(time.time()),
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "python": platform.python_version(),
    }

def network_snapshot() -> Dict[str, Any]:
    return {
        "ip_addr": _run(["ip", "addr"]),
        "routes": _run(["ip", "route"]),
        "listening": _run(["ss", "-tulpn"]),
    }

def disk_snapshot() -> Dict[str, Any]:
    return {
        "df": _run(["df", "-h"]),
    }
