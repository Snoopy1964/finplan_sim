from abc import ABC, abstractmethod
from datetime import date
import pandas as pd

class BaseComponent(ABC):
    @abstractmethod
    def simulate(self, start: date, end: date) -> pd.Series:
        pass