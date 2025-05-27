from datetime import date
import pandas as pd
from .base_component import BaseComponent

class ExpenseComponent(BaseComponent):
    def __init__(self, loan: float, living: float):
        self.loan = loan
        self.living = living

    def simulate(self, start: date, end: date) -> pd.Series:
        index = pd.date_range(start, end, freq="MS")
        return pd.Series(self.loan + self.living, index=index, name="expenses")