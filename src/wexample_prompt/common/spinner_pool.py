from __future__ import annotations

import threading
from typing import Dict, List, Optional

from wexample_prompt.const.spinners import DEFAULT_SPINNER_FRAMES


class Spinner:
    """Simple cyclic spinner.

    Not thread-safe; guard with external lock when used via SpinnerPool.
    """

    def __init__(self, frames: Optional[List[str]] = None) -> None:
        self.frames: List[str] = list(frames or DEFAULT_SPINNER_FRAMES)
        if not self.frames:
            self.frames = list(DEFAULT_SPINNER_FRAMES)
        self._idx: int = 0

    def next(self) -> str:
        if not self.frames:
            return ""
        ch = self.frames[self._idx]
        self._idx = (self._idx + 1) % len(self.frames)
        return ch

    def reset(self) -> None:
        self._idx = 0

    def set_frames(self, frames: List[str]) -> None:
        self.frames = list(frames) if frames else list(DEFAULT_SPINNER_FRAMES)
        self._idx = 0


class SpinnerPool:
    """Thread-safe pool for per-key spinners.

    Usage:
        from wexample_prompt.common.spinner_pool import SpinnerPool
        sym = SpinnerPool.next()  # default spinner
        sym = SpinnerPool.next("fs-build")  # named spinner, independent cycle
    """

    _lock = threading.RLock()
    _spinners: Dict[str, Spinner] = {}

    @classmethod
    def get(cls, key: str = "default") -> Spinner:
        with cls._lock:
            sp = cls._spinners.get(key)
            if sp is None:
                sp = Spinner()
                cls._spinners[key] = sp
            return sp

    @classmethod
    def next(cls, key: str = "default") -> str:
        with cls._lock:
            return cls.get(key).next()

    @classmethod
    def reset(cls, key: str = "default") -> None:
        with cls._lock:
            cls.get(key).reset()

    @classmethod
    def set_frames(cls, frames: List[str], key: str = "default") -> None:
        with cls._lock:
            cls.get(key).set_frames(frames)
