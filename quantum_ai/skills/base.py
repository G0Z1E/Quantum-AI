from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, runtime_checkable, Any, Dict

@dataclass
class SkillResult:
    ok: bool
    message: str
    data: Dict[str, Any] | None = None

@runtime_checkable
class Skill(Protocol):
    name: str
    description: str
    def run(self, ctx: Dict[str, Any]) -> SkillResult: ...
