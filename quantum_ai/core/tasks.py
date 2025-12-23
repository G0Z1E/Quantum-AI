from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, Optional
import time

@dataclass
class Task:
    name: str
    func: Callable[[Dict[str, Any]], Any]
    interval_sec: int = 60
    last_run: float = field(default=0.0)
    failures: int = field(default=0)

    def due(self) -> bool:
        return (time.time() - self.last_run) >= self.interval_sec

    def run(self, ctx: Dict[str, Any]) -> Any:
        self.last_run = time.time()
        return self.func(ctx)
