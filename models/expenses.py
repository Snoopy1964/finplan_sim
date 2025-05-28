from datetime import date
import pandas as pd
from models.base_component import BaseComponent
from utils.timeutils import date_range_index, zero_series

class ExpenseComponent(BaseComponent):
    def __init__(self, loan: float, living: float):
        self.loan = loan
        self.living = living

    def simulate(self, start: date, end: date) -> pd.Series:
        ts_index = date_range_index(start, end, freq="MS")

        return pd.Series(self.loan + self.living, index=ts_index, name="expenses")