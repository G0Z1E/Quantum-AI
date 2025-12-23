from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Any, List
import time

@dataclass
class Job:
    name: str
    every_sec: int
    action: Callable[[Dict[str, Any]], None]
    last_run: float = field(default=0.0)

    def due(self) -> bool:
        return (time.time() - self.last_run) >= self.every_sec

    def run(self, ctx: Dict[str, Any]) -> None:
        self.last_run = time.time()
        self.action(ctx)

class Scheduler:
    def __init__(self, jobs: List[Job]) -> None:
        self.jobs = jobs

    def loop(self, ctx: Dict[str, Any], once: bool = False) -> None:
        while True:
            for job in self.jobs:
                if job.due():
                    job.run(ctx)
            if once:
                return
            time.sleep(1)
