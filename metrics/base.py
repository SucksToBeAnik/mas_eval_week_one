from abc import ABC, abstractmethod
from typing import Dict

from custom_types import Trace


class MetricPlugin(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def compute(self, trace: Trace) -> float | Dict[str, float]:
        pass
