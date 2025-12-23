from __future__ import annotations
import logging
from dataclasses import dataclass, field
from typing import Dict, Any, List

from .memory import MemoryStore
from .supervisor import Supervisor
from .tasks import Task
from ..skills.base import Skill

log = logging.getLogger(__name__)

@dataclass
class QuantumEngine:
    memory: MemoryStore
    supervisor: Supervisor
    skills: Dict[str, Skill] = field(default_factory=dict)

    def register_skill(self, skill: Skill) -> None:
        self.skills[skill.name] = skill

    def list_skills(self) -> List[str]:
        return sorted(self.skills.keys())

    def run_skill(self, name: str, ctx: Dict[str, Any]) -> Dict[str, Any]:
        if name not in self.skills:
            raise KeyError(f"Unknown skill: {name}")
        res = self.skills[name].run(ctx)
        return {"skill": name, "ok": res.ok, "message": res.message, "data": res.data}

    def build_tasks(self) -> List[Task]:
        # Example recurring tasks
        return [
            Task(
                name="market_watch_tick",
                interval_sec=300,
                func=lambda ctx: self._task_market(ctx),
            ),
        ]

    def _task_market(self, ctx: Dict[str, Any]) -> None:
        out = self.run_skill("market_watch", ctx)
        self.memory.set("last_market_watch", out)
        self.memory.save()
        log.info("Saved market watch snapshot.")
