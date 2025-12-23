from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Dict, Any
import subprocess

from logger import setup_logger
from policy import CommandPolicy
from scheduler import Scheduler, Job
import sensors

def load_config(path: str) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    return json.loads(p.read_text(encoding="utf-8"))

def safe_exec(cmd: str, policy: CommandPolicy, logger, timeout: int = 30) -> Dict[str, Any]:
    if not policy.is_allowed(cmd):
        logger.warning("BLOCKED command: %s", cmd)
        return {"ok": False, "blocked": True, "cmd": cmd, "stdout": "", "stderr": "Blocked by policy"}

    logger.info("EXEC command: %s", cmd)
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, check=False)
    return {
        "ok": (p.returncode == 0),
        "blocked": False,
        "cmd": cmd,
        "rc": p.returncode,
        "stdout": (p.stdout or "").strip(),
        "stderr": (p.stderr or "").strip(),
    }

def job_host(ctx: Dict[str, Any]) -> None:
    snap = sensors.host_snapshot()
    ctx["logger"].info("HOST snapshot: %s", snap)

def job_net(ctx: Dict[str, Any]) -> None:
    snap = sensors.network_snapshot()
    ctx["logger"].info("NET snapshot collected (ip/route/ss).")

def job_disk(ctx: Dict[str, Any]) -> None:
    snap = sensors.disk_snapshot()
    ctx["logger"].info("DISK snapshot collected (df).")

def build_jobs(cfg: Dict[str, Any]) -> list[Job]:
    j = cfg.get("jobs", {})
    return [
        Job("host_snapshot", int(j.get("host_snapshot", 300)), job_host),
        Job("network_snapshot", int(j.get("network_snapshot", 300)), job_net),
        Job("disk_snapshot", int(j.get("disk_snapshot", 600)), job_disk),
    ]

def main() -> None:
    ap = argparse.ArgumentParser(prog="ShadowBot")
    ap.add_argument("--config", default="config.json", help="Path to config JSON")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("loop", help="Run scheduled monitoring jobs")
    run = sub.add_parser("run", help="Run a single safe command")
    run.add_argument("--exec", required=True, help='Command string, e.g. "uptime"')

    nmap = sub.add_parser("scan", help="Run authorized nmap scan")
    nmap.add_argument("--target", required=True)

    ap.add_argument("--once", action="store_true", help="Run one scheduler cycle then exit")
    args = ap.parse_args()

    cfg = load_config(args.config)
    logger = setup_logger(level=cfg.get("log_level", "INFO"))
    policy = CommandPolicy()

    ctx: Dict[str, Any] = {"logger": logger, "cfg": cfg, "policy": policy}

    if args.cmd == "run":
        out = safe_exec(args.exec, policy, logger)
        print(json.dumps(out, indent=2))
        return

    if args.cmd == "scan":
        target = args.target.strip()
        allowed = cfg.get("authorized_targets", [])
        if target not in allowed:
            logger.error("Target not authorized: %s", target)
            print(json.dumps({"ok": False, "error": "Target not authorized", "target": target}, indent=2))
            return

        nmap_args = cfg.get("nmap_args", ["nmap", "-Pn", "-sC", "-sV"])
        cmd = " ".join(nmap_args + [target])
        out = safe_exec(cmd, policy, logger, timeout=120)
        print(json.dumps(out, indent=2))
        return

    if args.cmd == "loop":
        sched = Scheduler(build_jobs(cfg))
        sched.loop(ctx, once=args.once)
        return

if __name__ == "__main__":
    main()
