from __future__ import annotations
import logging
from dataclasses import dataclass
from typing import Dict, Any, List
from .tasks import Task

log = logging.getLogger(__name__)

@dataclass
class Supervisor:
    max_failures: int = 3

    def run_loop(self, tasks: List[Task], ctx: Dict[str, Any], once: bool = False) -> None:
        import time
        while True:
            for task in tasks:
                if task.due():
                    try:
                        log.info("Running task=%s", task.name)
                        task.func(ctx)
                        task.failures = 0
                    except Exception as e:
                        task.failures += 1
                        log.exception("Task failed task=%s failures=%s err=%s", task.name, task.failures, e)
                        if task.failures >= self.max_failures:
                            self.self_heal(task, ctx)
                            task.failures = 0
            if once:
                return
            time.sleep(1)

    def self_heal(self, task: Task, ctx: Dict[str, Any]) -> None:
        # Self-healing placeholder: restart modules, reload config, rotate logs, etc.
        log.warning("Self-heal triggered for task=%s", task.name)
        ctx["self_heal_events"] = ctx.get("self_heal_events", 0) + 1
