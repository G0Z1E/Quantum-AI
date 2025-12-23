from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os

@dataclass(frozen=True)
class Settings:
    app_name: str = "QuantumAI"
    env: str = os.getenv("QUANTUM_ENV", "dev")
    data_dir: Path = Path(os.getenv("QUANTUM_DATA_DIR", "./.quantum_data")).resolve()
    log_level: str = os.getenv("QUANTUM_LOG_LEVEL", "INFO")
    memory_path: Path = data_dir / "memory.json"
    max_task_failures: int = int(os.getenv("QUANTUM_MAX_TASK_FAILURES", "3"))

def get_settings() -> Settings:
    s = Settings()
    s.data_dir.mkdir(parents=True, exist_ok=True)
    return s
