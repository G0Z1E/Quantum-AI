from __future__ import annotations
import logging
import subprocess
from dataclasses import dataclass
from typing import Dict, Any
from .base import SkillResult

log = logging.getLogger(__name__)

@dataclass
class ThreatScanSkill:
    name: str = "threat_scan"
    description: str = "Runs an authorized Nmap scan against targets (defensive)."

    def run(self, ctx: Dict[str, Any]) -> SkillResult:
        targets = ctx.get("targets", ["127.0.0.1"])
        nmap_args = ctx.get("nmap_args", ["nmap", "-Pn", "-sC", "-sV"])

        results = {}
        for t in targets:
            try:
                log.info("Scanning target=%s", t)
                proc = subprocess.run(
                    nmap_args + [t],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                results[t] = {
                    "rc": proc.returncode,
                    "stdout": proc.stdout,
                    "stderr": proc.stderr,
                }
            except Exception as e:
                return SkillResult(ok=False, message=f"Nmap scan failed for {t}: {e}")

        return SkillResult(ok=True, message="Threat scan completed.", data=results)
