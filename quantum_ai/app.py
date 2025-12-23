from __future__ import annotations
import argparse
import json
import logging

from quantum_ai.config import get_settings
from quantum_ai.utils.log import setup_logging
from quantum_ai.core.memory import MemoryStore
from quantum_ai.core.supervisor import Supervisor
from quantum_ai.core.engine import QuantumEngine

from quantum_ai.skills.threat_scan import ThreatScanSkill
from quantum_ai.skills.market_watch import MarketWatchSkill

log = logging.getLogger(__name__)

def build_engine() -> QuantumEngine:
    s = get_settings()
    setup_logging(s.log_level)

    mem = MemoryStore(path=s.memory_path)
    mem.load()

    engine = QuantumEngine(
        memory=mem,
        supervisor=Supervisor(max_failures=s.max_task_failures),
    )

    # Register skills
    engine.register_skill(ThreatScanSkill())
    engine.register_skill(MarketWatchSkill())

    return engine

def main() -> None:
    engine = build_engine()
    s = get_settings()

    p = argparse.ArgumentParser(prog=s.app_name)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("skills", help="List installed skills")

    run = sub.add_parser("run", help="Run one skill once")
    run.add_argument("--skill", required=True)
    run.add_argument("--ctx", default="{}", help='JSON context, e.g. \'{"targets":["192.168.1.10"]}\'')

    loop = sub.add_parser("loop", help="Run supervisor loop (recurring tasks)")
    loop.add_argument("--once", action="store_true", help="Run one cycle then exit")

    args = p.parse_args()

    if args.cmd == "skills":
        print("\n".join(engine.list_skills()))
        return

    if args.cmd == "run":
        ctx = json.loads(args.ctx)
        out = engine.run_skill(args.skill, ctx)
        print(json.dumps(out, indent=2))
        return

    if args.cmd == "loop":
        tasks = engine.build_tasks()
        ctx = {"watchlist": ["MSTY", "SPY", "QQQ"]}
        engine.supervisor.run_loop(tasks, ctx, once=args.once)
        return

if __name__ == "__main__":
    main()
