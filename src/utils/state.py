
import time
from dataclasses import dataclass, field

@dataclass
class RateLimiter:
    cooldown_s: float
    max_per_hour: int
    last_ts: float = 0.0
    history: list = field(default_factory=list)

    def allow(self) -> bool:
        now = time.time()
        self.history = [t for t in self.history if now - t < 3600]
        if (now - self.last_ts) < self.cooldown_s:
            return False
        if len(self.history) >= self.max_per_hour:
            return False
        self.last_ts = now
        self.history.append(now)
        return True
